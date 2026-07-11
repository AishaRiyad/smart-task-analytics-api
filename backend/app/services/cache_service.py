import json
from typing import Any

import redis.asyncio as redis

from app.core.config import settings


redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


async def get_cache(key: str) -> Any | None:
    try:
        cached_data = await redis_client.get(key)

        if cached_data is None:
            return None

        return json.loads(cached_data)

    except redis.RedisError:
        return None


async def set_cache(
    key: str,
    value: Any,
    expire_seconds: int = 60,
) -> None:
    try:
        await redis_client.set(
            key,
            json.dumps(value),
            ex=expire_seconds,
        )

    except redis.RedisError:
        pass


async def delete_cache(key: str) -> None:
    try:
        await redis_client.delete(key)

    except redis.RedisError:
        pass


async def close_redis() -> None:
    await redis_client.aclose()