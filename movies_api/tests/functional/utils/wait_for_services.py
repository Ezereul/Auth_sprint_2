import asyncio
from logging import getLogger

import backoff
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from movies_api.tests.functional.settings import test_base_settings

logger = getLogger(__name__)


@backoff.on_exception(backoff.expo, Exception, max_time=300, max_tries=10)
async def wait_for_redis() -> None:
    logger.info("Pinging Redis...")
    client = Redis(host=test_base_settings.redis_host, port=test_base_settings.redis_port)
    try:
        await client.ping()
        logger.info("Redis is up!")
    finally:
        await client.close()


@backoff.on_exception(backoff.expo, Exception, max_time=300, max_tries=10)
async def wait_for_elasticsearch() -> None:
    logger.info("Pinging Elastic...")
    client = AsyncElasticsearch([{'host': test_base_settings.es_host, 'port': test_base_settings.es_port}])
    try:
        await client.indices.exists(index='ping')
        logger.info("Elasticsearch is up!")
    finally:
        await client.close()


async def main():
    await asyncio.gather(
        wait_for_redis(),
        wait_for_elasticsearch(),
    )


if __name__ == '__main__':
    logger.info("Waiting for Redis to start...")
    logger.info("Waiting for Elastic to start...")
    asyncio.run(main())
