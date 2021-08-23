import pytest
from fastapi import status
from httpx import AsyncClient

BASE_URL = "http://monochrome.test"


class TestRootRedirect:
    @pytest.mark.asyncio
    async def test_root_redirect(self, client: AsyncClient):
        # Redirect to the API docs
        response = await client.get("/", allow_redirects=False)
        assert (
            response.status_code == status.HTTP_301_MOVED_PERMANENTLY
            and response.next_request.url == f"{BASE_URL}/docs"
        )

    @pytest.mark.asyncio
    async def test_ping(self, client: AsyncClient):
        # Redirect to the API docs
        response = await client.get("/ping")
        assert response.text == '"pong"'
