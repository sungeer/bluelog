import redis.asyncio as redis

from viper.core import settings


def redis_conn(host=settings.CONF.get_conf('REDIS', 'HOST'), port=6379, db=0, decode_responses=False):
    return redis.Redis(
        host=host,
        port=port,
        db=db,
        # password=settings.CONF.get_sec_conf('REDIS', 'PASSWD'),
        decode_responses=decode_responses
    )


redis_client = redis_conn(decode_responses=True)


async def close_redis():
    await redis_client.aclose()
