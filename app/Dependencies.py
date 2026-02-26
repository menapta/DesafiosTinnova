from app.RedisClient import redisConnection
from app.Cache import RedisCache 


_cache_client = RedisCache(redisConnection())

def getCacheClient():
    return _cache_client