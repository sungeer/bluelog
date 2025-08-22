from contextlib import asynccontextmanager

from viper.utils import http_util, redis_util, pools


@asynccontextmanager
async def register_events(app):
    pass
    yield
    await http_util.close_httpx()
    await redis_util.close_redis()
    pools.close_threads()
