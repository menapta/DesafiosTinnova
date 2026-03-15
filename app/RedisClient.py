# import redis

# def redisConnection() -> redis.Redis:
#     pool = redis.ConnectionPool(
#         host="localhost",
#         port="6379",
#         db=0
#     )
#     return redis.Redis(connection_pool=pool)
import os
import redis

def redisConnection() -> redis.Redis:
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    return redis.Redis(host=host, port=port)