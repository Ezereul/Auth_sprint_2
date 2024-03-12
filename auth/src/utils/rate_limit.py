import time

from redis.asyncio import Redis
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Request


REQUEST_LIMIT_PER_MINUTE = 20
DURATION = 60


async def is_request_allowed(user_id: str, redis: Redis):
    current_timestamp = time.time()
    window_start_timestamp = current_timestamp - DURATION
    key = f"rate_limit:{user_id}"

    p = redis.pipeline()
    await p.zremrangebyscore(key, 0, window_start_timestamp)
    await p.zcount(key, window_start_timestamp, current_timestamp)
    await p.zadd(key, {current_timestamp: current_timestamp})
    await p.expire(key, DURATION)

    _, current_count, _, _ = await p.execute()

    if current_count < REQUEST_LIMIT_PER_MINUTE:
        return True
    else:
        await redis.zrem(key, current_timestamp)
        return False


async def extract_user_id(request: Request) -> str:
    try:
        Authorize = AuthJWT(request)
        await Authorize.jwt_required()
        user_id = await Authorize.get_jwt_subject()
        if user_id:
            return f"authenticated:{user_id}"
    except Exception as e:
        pass

    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    return f"ip:{ip_address}:{user_agent}"
