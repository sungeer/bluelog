import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

thread_pool_db = ThreadPoolExecutor(max_workers=2)


async def run_in_thread_pool_db(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    bound_func = partial(func, *args, **kwargs)
    return await loop.run_in_executor(thread_pool_db, bound_func)  # noqa


thread_pool_delay = ThreadPoolExecutor()


async def run_in_thread_pool_delay(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    bound_func = partial(func, *args, **kwargs)
    return await loop.run_in_executor(thread_pool_db, bound_func)  # noqa


def close_threads():
    thread_pool_db.shutdown()
    thread_pool_delay.shutdown()
