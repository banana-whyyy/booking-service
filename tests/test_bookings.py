import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_booking_without_auth(client: AsyncClient, test_room):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    response = await client.post(
        "/bookings",
        json={
            "room_id": test_room.id,
            "time_start": start_time.isoformat(),
            "time_end": end_time.isoformat()
            },
        )

    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


@pytest.mark.asyncio
async def test_booking_with_auth(client: AsyncClient, test_room, user_access_token):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)

    response = await client.post(
        "/bookings",
        json={
            "room_id": test_room.id,
            "time_start": start_time.isoformat(),
            "time_end": end_time.isoformat()
        },
        headers={"Authorization": f"Bearer {user_access_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data


@pytest.mark.asyncio
async def test_create_booking_time_conflict(
    client: AsyncClient,
    test_booking,
    test_room,
    user_access_token
):
    response = await client.post(
        "/bookings",
        json={
            "room_id": test_room.id,
            "time_start": test_booking.time_start.isoformat(),
            "time_end": test_booking.time_end.isoformat(),
        },
        headers={"Authorization": f"Bearer {user_access_token}"},
    )

    assert response.status_code == 409