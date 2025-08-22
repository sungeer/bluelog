import httpx

from viper.core import settings

limits = httpx.Limits(
    max_keepalive_connections=settings.CONF.get_int_conf('HTTPX', 'POOL_SIZE_COMMON'),
    max_connections=settings.CONF.get_int_conf('HTTPX', 'MAX_OVERFLOW_COMMON')
)

timeout = httpx.Timeout(
    connect=2.0,
    read=5.0,  # 从发送请求到接收完整响应数据的时间
    write=2.0,
    pool=2.0
)

httpx_common = httpx.AsyncClient(limits=limits, timeout=timeout)

# 流式
limits = httpx.Limits(
    max_keepalive_connections=settings.CONF.get_int_conf('HTTPX', 'POOL_SIZE_STREAM'),
    max_connections=settings.CONF.get_int_conf('HTTPX', 'MAX_OVERFLOW_STREAM')
)

timeout = httpx.Timeout(
    connect=3.0,  # 建立连接的时间
    read=10.0,  # 等待每个数据块的时间
    write=3.0,  # 向服务器发送完数据的时间
    pool=2.0  # 从连接池中获取连接的时间
)

httpx_stream = httpx.AsyncClient(limits=limits, timeout=timeout)


async def close_httpx():
    await httpx_common.aclose()
    await httpx_stream.aclose()
