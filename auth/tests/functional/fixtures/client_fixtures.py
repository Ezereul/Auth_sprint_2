import pytest_asyncio
from httpx import AsyncClient
import http

from auth.src.main import app


@pytest_asyncio.fixture
async def client_fixture(app_with_overridden_redis, app_with_overridden_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def authenticated_client(client_fixture, user_fixture):
    login_data = {"username": user_fixture.username, "password": "testpassword"}
    response = await client_fixture.post("/auth/login", json=login_data)
    assert response.status_code == http.HTTPStatus.OK
    cookies = response.cookies
    client_fixture.cookies = cookies
    yield client_fixture


@pytest_asyncio.fixture
async def superuser_authenticated_client(client_fixture, superuser_fixture):
    login_data = {"username": superuser_fixture.username, "password": "testpassword"}
    response = await client_fixture.post("/auth/login", json=login_data)
    assert response.status_code == http.HTTPStatus.OK
    cookies = response.cookies
    client_fixture.cookies = cookies
    yield client_fixture


@pytest_asyncio.fixture
async def client_factory(request, client_fixture, user_fixture, superuser_fixture):
    if request.param == "user":
        login_data = {"username": user_fixture.username, "password": "testpassword"}
    elif request.param == "superuser":
        login_data = {"username": superuser_fixture.username, "password": "testpassword"}
    else:
        raise ValueError("Invalid user type")

    response = await client_fixture.post("/auth/login", json=login_data)
    assert response.status_code == http.HTTPStatus.OK
    cookies = response.cookies
    client_fixture.cookies = cookies
    yield client_fixture
