import redis

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    # password=None,
    max_connections=100,  # 限制池大小
    socket_timeout=2,
    socket_connect_timeout=2,
    health_check_interval=30,  # 定期发 PING 维持连接可用性
    decode_responses=True  # 返回 str 而不是 bytes
)

# 在进程内复用同一个 Redis 客户端实例
redis_conn = redis.Redis(connection_pool=pool)


if __name__ == '__main__':
    redis_conn.set('k', 'v')
    print(redis_conn.get('k'))
