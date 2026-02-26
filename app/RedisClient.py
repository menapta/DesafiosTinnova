import redis

def redisConnection() -> redis.Redis:
    pool = redis.ConnectionPool(
        host="localhost",
        port="6379",
        db=0
    )
    return redis.Redis(connection_pool=pool)
