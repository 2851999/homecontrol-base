import asyncio
from typing import Any, Callable, Coroutine


def run_until_complete(
    function: Callable[[], Coroutine[Any, Any, Any]], **params
) -> Any:
    """Runs the given asynchronous method until completion

    Args:
        function (Coroutine[Any, Any, Any]): Function that returns a coroutine to await

    Returns:
        Whatever was returned by the function's coroutine

    Not the most ideal way to deal with midea-ng's async capabilities,
    but ensures it remains functional without async methods
    """

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # Temp fix for running under FastAPI
        # TODO: really should just let midea be async, then use this if want
        # separate script
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def async_func():
        return await function(**params)

    coroutine = async_func()
    result = loop.run_until_complete(coroutine)
    return result
