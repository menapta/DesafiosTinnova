from typing import cast

import redis



class Cache:
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
