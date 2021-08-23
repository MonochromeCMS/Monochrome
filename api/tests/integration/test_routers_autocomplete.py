import pytest
from fastapi import status
from httpx import AsyncClient


class TestAutocomplete:
    @pytest.mark.asyncio
    async def test_empty_groups(self, client: AsyncClient, headers: dict):
        # Return a list with only ["no group"] if no groups have been provided yet
        response = await client.get("/autocomplete/groups", headers=headers)
        assert response.json() == ["no group"]
