import asyncio

import pytest_asyncio

pytest_plugins = [
    "auth.tests.functional.fixtures.db_fixtures",
    "auth.tests.functional.fixtures.redis_fixtures",
    "auth.tests.functional.fixtures.client_fixtures",
    "auth.tests.functional.fixtures.data_fixtures"
]


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
