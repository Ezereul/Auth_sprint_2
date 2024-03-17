from typing import Optional

from redis.asyncio import Redis

redis_tokens: Optional[Redis] = None
redis_rate_limit: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis_tokens


async def get_redis_rate_limit() -> Redis:
    return redis_rate_limit
