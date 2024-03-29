import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from redis.asyncio import Redis
import logging

from movies_api.src.core.logger import setup_logging
from movies_api.src.api.v1 import films, genres, persons
from movies_api.src.core.api_settings import settings
from movies_api.src.db import _redis, elastic


setup_logging()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/movies/openapi',
    openapi_url='/api/movies/openapi.json',
    default_response_class=ORJSONResponse,
    description='Information regarding films, genres and people who took part in the films creation',
    version=settings.version
)


@app.on_event('startup')
async def startup():
    logging.debug('Config: %s', vars(settings))
    _redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.es_host}:{settings.es_port}'])


@app.on_event('shutdown')
async def shutdown():
    await _redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
