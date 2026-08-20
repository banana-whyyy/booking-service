import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_room_as_admin(client: AsyncClient, admin_access_token):
    response = await client.post(
        "/rooms",
        json={
            "name": "Room2",
            "description": "string",
            "price_hour": 15,
            "capacity": 5,
            "has_projector": False,
            "has_whiteboard": False
        },
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data


@pytest.mark.asyncio
async def test_create_room_as_user_forbidden(client: AsyncClient, user_access_token):
    response = await client.post(
        "/rooms",
        json={
            "name": "Room2",
            "description": "string",
            "price_hour": 15,
            "capacity": 5,
            "has_projector": False,
            "has_whiteboard": False
        },
        headers={"Authorization": f"Bearer {user_access_token}"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_room_unauthorized(client: AsyncClient):
    response = await client.post(
        "/rooms",
        json={
            "name": "Room2",
            "description": "string",
            "price_hour": 15,
            "capacity": 5,
            "has_projector": False,
            "has_whiteboard": False
        },
    )
    assert response.status_code == 401