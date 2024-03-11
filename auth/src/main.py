from contextlib import asynccontextmanager

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from auth.src.api.errors import account_exception_handler, authjwt_exception_handler
from auth.src.api.middlewares import rate_limit_middleware
from auth.src.api.routers import main_router
from auth.src.core import logger
from auth.src.core.config import settings
from auth.src.db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port, decode_responses=True)
    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    lifespan=lifespan,
    log_config=logger.LOGGING_DICT_CONFIG,
    log_level=settings.logger.level,
    default_response_class=JSONResponse,
)
app.add_exception_handler(AuthJWTException, authjwt_exception_handler)
app.add_exception_handler(ValueError, account_exception_handler)
app.include_router(main_router)
app.middleware("http")(rate_limit_middleware)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
