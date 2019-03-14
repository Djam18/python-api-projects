import redis
import json

_memory_cache = {}


class RedisCache:
    def __init__(self, host='localhost', port=6379):
        try:
            self.r = redis.Redis(host=host, port=port, decode_responses=True)
            self.r.ping()
            self.available = True
        except Exception:
            self.r = None
            self.available = False

    def get(self, key):
        if self.available and self.r:
            val = self.r.get(key)
            return val
        return _memory_cache.get(key)

    def set(self, key, value, ttl=3600):
        if self.available and self.r:
            self.r.setex(key, ttl, value)
        else:
            _memory_cache[key] = value
