import asyncio
import pytest_asyncio


pytest_plugins = [
    "movies_api.tests.functional.fixtures.es_fixtures",
    "movies_api.tests.functional.fixtures.redis_fixtures",
    "movies_api.tests.functional.fixtures.client_fixtures",
    "movies_api.tests.functional.fixtures.data_factories"
]


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
