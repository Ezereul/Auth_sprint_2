from redis.asyncio import Redis

redis_tokens: Redis | None = None
redis_rate_limit: Redis | None = None


async def get_redis() -> Redis:
    return redis_tokens


async def get_redis_rate_limit() -> Redis:
    return redis_rate_limit
