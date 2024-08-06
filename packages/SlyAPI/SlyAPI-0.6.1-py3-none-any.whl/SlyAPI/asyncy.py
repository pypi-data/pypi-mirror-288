'''Useful classes and functions for asynchronous programming.'''
import asyncio
import functools
from typing import Generic, ParamSpec, TypeAlias, TypeVar, Callable, Generator, AsyncGenerator, Any
from contextlib import AbstractAsyncContextManager

T = TypeVar('T')
U = TypeVar('U')

T_Params = ParamSpec("T_Params")
U_Params = ParamSpec("U_Params")

unmanaged_tasks: set[Any] = set()
def unmanage_async_context(context: AbstractAsyncContextManager[T]) -> tuple[asyncio.Task[T], asyncio.Event]:
    '''
    Extract an async context manager's value without manually managing its lifetime.
    The context manager is entered until `set()` is called on the returned event.

    thats it *unmanages your async context manager*
    '''
    close_context = asyncio.Event()
    fut_T_ready = asyncio.Event()
    fut_T = None
    async def background():
        async with context as inner:
            nonlocal fut_T
            fut_T = inner
            fut_T_ready.set()
            # print(f'Released event for {context}')
            await close_context.wait()
    task = asyncio.create_task(background())
    unmanaged_tasks.add(task)
    task.add_done_callback(unmanaged_tasks.remove)
    async def aenter_wait():
        await fut_T_ready.wait()
        assert fut_T is not None
        return fut_T
    return (
        asyncio.create_task(aenter_wait()),
        close_context )

class AsyncLazy(Generic[T]):
    '''
    Async iterator which does not accumulate any results unless awaited.
    Awaiting instances will return a list of the results.
    '''
    gen: AsyncGenerator[T, None]

    def __init__(self, gen: AsyncGenerator[T, None]):
        self.gen = gen

    def __aiter__(self) -> AsyncGenerator[T, None]:
        return self.gen

    async def _items(self) -> list[T]:
        return [t async for t in self.gen]

    def __await__(self) -> Generator[Any, None, list[T]]:
        '''Yield the aggregate results of the generator as a list.'''
        return self._items().__await__()

    def map(self, f: Callable[[T], U]) -> 'AsyncLazy[U]':
        '''Apply a function to each item that is yielded.'''
        return AsyncLazy(f(x) async for x in self)

    @classmethod
    def wrap(cls, fn: Callable[T_Params, AsyncGenerator[T, None]]):
        '''Convert an async generator async function to return an AsyncLazy instance.'''
        @functools.wraps(fn)
        def wrapped(*args: T_Params.args, **kwargs: T_Params.kwargs) -> AsyncLazy[T]:
            return AsyncLazy(fn(*args, **kwargs))
        return wrapped
    
AsyncTrans: TypeAlias = AsyncLazy