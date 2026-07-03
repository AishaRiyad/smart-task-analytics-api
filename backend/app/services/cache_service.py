import json
import redis

from app.core.config import settings


redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True
)


def get_cache(key: str):
    try:
        cached_data = redis_client.get(key)

        if cached_data:
            return json.loads(cached_data)

        return None
    except redis.RedisError:
        return None


def set_cache(key: str, value, expire_seconds: int = 60):
    try:
        redis_client.setex(
            key,
            expire_seconds,
            json.dumps(value)
        )
    except redis.RedisError:
        pass


def delete_cache(key: str):
    try:
        redis_client.delete(key)
    except redis.RedisError:
        pass