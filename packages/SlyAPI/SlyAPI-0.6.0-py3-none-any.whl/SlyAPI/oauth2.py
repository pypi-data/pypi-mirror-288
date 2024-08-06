'''
Implementation for OAuth2.0 with PKCE as the `Auth` interface
https://datatracker.ietf.org/doc/html/rfc7636
'''
import asyncio
import base64
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from hashlib import sha256
import json
import secrets
from copy import copy
from typing import Any, Callable, ParamSpec, TypeVar, cast

from warnings import warn

from .auth import Auth
from .web import ApiError, JsonMap, Request, TomlMap, serve_once


import aiohttp
from aiohttp import ClientSession as Client

import urllib.parse

F_Params = ParamSpec('F_Params')
F_Return = TypeVar('F_Return')

# currently just a marker and has no effect
def requires_scopes(*_scopes: str) -> Callable[[Callable[F_Params, F_Return]], Callable[F_Params, F_Return]]:
    'Mark a endpoint as requiring specific scopes to be used'
    def wrap(func: Callable[F_Params, F_Return]) -> Callable[F_Params, F_Return]:
        return func
    return wrap

@dataclass
class OAuth2User:
    token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = 'Bearer'
    scopes: list[str] = field(default_factory=list)
            
    @classmethod
    def from_json_obj(cls, obj: TomlMap) -> 'OAuth2User':
        '''Read an app from a JSON object'''
        match obj:
            case { # JSON / self.to_dict()
                'token': str(token),
                'refresh_token': str(refresh_token),
                'expires_at': str(expires_at_str),
                'token_type': str(token_type),
                'scopes': scopes
            }:
                try:
                    expires_at = datetime.strptime(expires_at_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    expires_at = datetime.strptime(expires_at_str, '%Y-%m-%dT%H:%M:%SZ')
                return cls(token, refresh_token, expires_at, token_type, cast(list[str], scopes))
            case { # asdict(self)
                   # TODO: eliminate this case?
                'token': str(token),
                'refresh_token': str(refresh_token),
                'expires_at': datetime() as expires_at,
                'token_type': str(token_type),
                'scopes': scopes
            }:
                return cls(token, refresh_token, expires_at, token_type, cast(list[str], scopes))
            case {
                'access_token': str(token),
                'expires_in': str(expires_in) | int(expires_in),
                'token_type': str(token_type),
                **others
            }: # OAuth 2 grant response
                expires_in = int(expires_in)
                expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                refresh_token = others.get('refresh_token', '')
                scopes = cast(str, others.get('scope', '')).split(' ')
                if refresh_token is None:
                    warn(
                        "Google doesn't re-issue refresh tokens when you authorize a new token from the same application for the same user. That might be the case here, since a token grant was recieved without `refresh_token`! Refreshing these credentials will fail, consider revoking access at https://myaccount.google.com/permissions and re-authorizing."
                    )
                return cls(token, cast(str, refresh_token), expires_at, token_type, scopes)
            case { # mastodon
                'access_token': str(token),
                'token_type': str(token_type),
                'scope': str(scopes),
                'created_at': int(_stamp)
            }:
                expires_at = datetime(2400, 1, 1) # TODO: does this never expire?
                return cls(token, '', expires_at, token_type, scopes.split(' '))
            case _:
                raise ValueError(F"Unknown format for OAuth2User: {obj}")

    @classmethod
    def from_json_file(cls, path: str) -> 'OAuth2User':
        '''Read an app from a JSON file path'''
        with open(path, 'rb') as f:
            return cls.from_json_obj(json.load(f))

    def to_dict(self) -> dict[str, Any]:
        return {
            'token': self.token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'token_type': self.token_type,
            'scopes': self.scopes
        }

@dataclass
class OAuth2App:
    id: str
    secret: str
    auth_uri: str # flow step 1
    token_uri: str # flow step 3

    @classmethod
    def from_json_obj(cls, obj: JsonMap) -> 'OAuth2App':
        '''Read an app from a JSON object, either from the Google Console JSON format or a set of kwargs'''
        match obj:
            case { # to_dict(self)
                'id': str(id),
                'secret': str(secret),
                'auth_uri': str(auth_uri),
                'token_uri': str(token_uri)
            } | { # Google JSON
                'web': {
                    'client_id': str(id),
                    'client_secret': str(secret),
                    'auth_uri': str(auth_uri),
                    'token_uri': str(token_uri)
                }
            }: 
                return cls(id, secret, auth_uri, token_uri)
            case _:
                raise ValueError(F"Unknown format for OAuth2App: {obj}")

    @classmethod
    def from_json_file(cls, path: str) -> 'OAuth2App':
        '''Read an app from a JSON file path'''
        with open(path, 'rb') as f:
            return cls.from_json_obj(json.load(f))

    def auth_url_with_pkce(self, redirect_uri: str, state: str, scopes: str) -> tuple[str, str, str]:
        state_challenge = secrets.token_urlsafe(54)
        code_verifier = secrets.token_urlsafe(54)
        verifier_hash = sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(verifier_hash).decode('utf-8').rstrip('=')
        params = {
            'client_id': self.id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'state': state+state_challenge,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'scope': scopes,
            'access_type': 'offline',
            'prompt': 'consent', # re-issue refresh tokens!
            }
        return F"{self.auth_uri}?{urllib.parse.urlencode(params)}", code_verifier, state_challenge

    async def refresh(self, client: Client, user: OAuth2User):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': user.refresh_token,
            'client_id': self.id,
            'client_secret': self.secret,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        async with client.post(self.token_uri, data=data, headers=headers) as resp:
            if resp.status != 200:
                raise await ApiError.from_resposnse(resp)
            result = await resp.json()

        match result:
            case {
                'access_token': token,
                'expires_in': expires_str,
                'token_type': token_type,
                **_others
            }: # OAuth 2 refresh response
                expiry = datetime.utcnow() + timedelta(seconds=int(expires_str))
                new_user = copy(user)
                new_user.token = token
                new_user.expires_at = expiry
                new_user.token_type = token_type
            case _:
                raise ValueError(F"Invalid OAuth2 refresh response: {result}")
        return new_user
    
    async def exchange_code(self, code: str, verifier: str, scopes: list[str], redirect_uri: str, client: Client|None=None) -> OAuth2User:
        grant_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.id,
            'redirect_uri': redirect_uri,
            'scope': scopes,
            'code_verifier': verifier,
        }
        grant_headers = {
            'Authorization': F"Basic {base64.b64encode(F'{self.id}:{self.secret}'.encode('utf-8')).decode('utf-8')}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        if client is None:
            do_req = aiohttp.request
        else:
            do_req = client.request

        async with do_req('POST', self.token_uri, data=grant_data, headers=grant_headers) as resp:
            if resp.status != 200:
                raise await ApiError.from_resposnse(resp)
            result = await resp.json()
            user = OAuth2User.from_json_obj(result)

        return user

@dataclass
class OAuth2(Auth):
    """Provides the Auth interface implementation for OAuth2"""
    app: OAuth2App
    user: OAuth2User

    _refreshed: asyncio.Semaphore
    _refresh_callback: Callable[[OAuth2User], None] | None = None

    def __init__(self, app: OAuth2App|str, user: OAuth2User|str,
        on_refresh: Callable[[OAuth2User], None] | None = None):
        """Load an OAuth2 app and user from JSON files or existing objects."""
        if isinstance(app, str):
            app = OAuth2App.from_json_file(app)
        if isinstance(user, str):
            user = OAuth2User.from_json_file(user)
        self.app = app
        self.user = user
        self._refresh_callback = on_refresh
        self._refreshed = asyncio.Semaphore()
    
    async def sign(self, client: Client, request: Request) -> Request:
        await self._refreshed.acquire()
        if datetime.utcnow() > self.user.expires_at:
            # TODO: log refresh
            self.user = await self.app.refresh(client, self.user)
        self._refreshed.release()
        request.headers['Authorization'] = F"{self.user.token_type} {self.user.token}"
        return request
         
    

async def command_line_oauth2(
        app: OAuth2App,
        redirect_host: str,
        redirect_port: int,
        usePin: bool,
        scopes: list[str]
        ) -> OAuth2User:
    import webbrowser

    redirect_uri = F'http://{redirect_host}:{redirect_port}'

    # step 1: get the user to authorize the application
    grant_link, verifier, state = app.auth_url_with_pkce(redirect_uri, '', ' '.join(scopes))

    if usePin or not webbrowser.open(grant_link, new=1, autoraise=True):
        print("Please open the following link in your browser:")
        print(grant_link)
        print("Then enter the code below:")
        code = input("code")
    else:
        # step 2: wait for the user to be redirected with the code
        query = await serve_once(redirect_host, redirect_port, 'step2.html')

        # challenge is state[-54:], but state is explicitly ''
        # BUT 54 is LENGTH IN BYTES OF RAW CHALLENGE, *NOT* the length of the base64-encoded challenge
        if 'state' not in query:
            raise PermissionError("Redirect did not return any state parameter.")
        elif query['state'] != state:
            raise PermissionError("Redirect did not return the correct state parameter.")
        elif 'code' not in query:
            raise PermissionError("Redirect did authorize grant.")
        code = query['code']

    # step 3: exchange the code for access token
    return await app.exchange_code(code, verifier, scopes, redirect_uri)