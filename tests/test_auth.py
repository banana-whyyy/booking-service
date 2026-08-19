import pytest
import asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, test_user, user_refresh_token):
    await asyncio.sleep(1.01)

    response = await client.post(
        "/auth/refresh",
        params={"refresh_token": user_refresh_token}
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    response = await client.post(
        "/auth/refresh",
        params={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401