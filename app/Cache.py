from typing import cast
import os

import redis



class Cache:
    def __init__(self):
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_client = redis.Redis(host=host, port=port)

    def get(self, key: str) -> bytes | None:
        raise NotImplementedError

    def set(self, key: str, value: bytes, ex: int | None = None) -> None:
        raise NotImplementedError


class RedisCache(Cache):
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def get(self, key: str) -> bytes | None:
        return cast(bytes | None, self.redis_client.get(key))

    def set(self, key: str, value: bytes, ex: int | None = None) -> None:
        self.redis_client.set(key, value, ex=ex)
