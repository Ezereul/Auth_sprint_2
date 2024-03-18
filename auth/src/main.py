from contextlib import asynccontextmanager

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis

from auth.src.api.errors import account_exception_handler, authjwt_exception_handler
from auth.src.api.middlewares import check_x_request_middleware, rate_limit_middleware
from auth.src.api.routers import main_router
from auth.src.api.tracers import setup_tracing
from auth.src.core import logger
from auth.src.core.config import settings
from auth.src.core.logger import setup_logging
from auth.src.db import redis

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis_tokens = Redis(
        host=settings.redis.host, port=settings.redis.port, decode_responses=True, db=0)
    redis.redis_rate_limit = Redis(
        host=settings.redis.host, port=settings.redis.port, decode_responses=True, db=1)
    yield
    await redis.redis_tokens.aclose()
    await redis.redis_rate_limit.aclose()


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    lifespan=lifespan,
    log_config=logger.LOGGING_DICT_CONFIG,
    log_level=settings.logger.level,
    default_response_class=JSONResponse,
    docs_url='/api/auth/openapi',
    openapi_url='/api/auth/openapi.json',
)
app.add_exception_handler(AuthJWTException, authjwt_exception_handler)
app.add_exception_handler(ValueError, account_exception_handler)
app.include_router(main_router)
app.middleware("http")(rate_limit_middleware)

if settings.enable_tracing:
    setup_tracing()
    app.middleware("http")(check_x_request_middleware)
    FastAPIInstrumentor.instrument_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
