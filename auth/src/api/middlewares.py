from typing import Callable

from fastapi import Request, Response

from auth.src.db.redis import get_redis_rate_limit
from auth.src.utils.rate_limit import is_request_allowed, extract_user_id


async def rate_limit_middleware(request: Request, call_next: Callable):
    redis_instance = await get_redis_rate_limit()
    user_id = await extract_user_id(request)

    is_allowed = await is_request_allowed(user_id, redis_instance)
    print(is_allowed)
    if not is_allowed:
        return Response(content="Too Many Requests", status_code=429)

    response = await call_next(request)
    return response