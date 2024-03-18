from http import HTTPStatus
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse

from auth.src.db.redis import get_redis_rate_limit
from auth.src.utils.rate_limit import extract_user_id, is_request_allowed


async def rate_limit_middleware(request: Request, call_next: Callable):
    redis_instance = await get_redis_rate_limit()
    user_id = await extract_user_id(request)

    is_allowed = await is_request_allowed(user_id, redis_instance)
    if not is_allowed:
        return Response(content="Too Many Requests", status_code=HTTPStatus.TOO_MANY_REQUESTS)

    response = await call_next(request)
    return response


async def check_x_request_middleware(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
    return response
