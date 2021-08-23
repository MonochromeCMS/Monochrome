import pytest
import asyncio
from httpx import AsyncClient
from datetime import timedelta

from api.main import app
from api.routers.auth import create_access_token

USER_ID = "c603ef4f-08f9-4130-a770-3a34defa44b3"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://monochrome.test") as c:
        yield c


@pytest.fixture(scope="session")
def token():
    return "Bearer " + create_access_token(data={"sub": USER_ID}, expires_delta=timedelta(minutes=5))


@pytest.fixture(scope="session")
def headers(token):
    return dict(Authorization=token)
