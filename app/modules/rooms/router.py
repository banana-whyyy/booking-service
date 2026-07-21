from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_room_by_name, create_room, room_update, room_delete, get_room
from .schemas import RoomCreate, RoomResponse, RoomUpdate, RoomFilterParams
from app.database import get_db
from app.dependencies import get_admin_user
from ..auth.models import User
from ..bookings.services import get_available_rooms


room = APIRouter(tags=["rooms"], prefix="/rooms")


@room.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def add_room(
    room: RoomCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    if await get_room_by_name(db, room.name):
        raise HTTPException(
            status_code=status.HTTP_409_BAD_REQUEST,
            detail="Room with this name already exists",
        )
    new_room = await create_room(db, room)
    await db.commit()
    await db.refresh(new_room)
    return new_room


@room.get("/filters", response_model=list[RoomResponse])
async def get_filters_rooms(
    filters: RoomFilterParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    rooms = await get_available_rooms(db=db, filters=filters)
    return rooms


@room.get("/{room_id}", response_model=RoomResponse)
async def read_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    room = await get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return room


@room.put("/{room_id}", response_model=RoomResponse)
async def modify_room(
    room_id: int,
    room_modify: RoomUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    updated = await room_update(db, room_id, room_modify)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return updated


@room.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    success = await room_delete(db, room_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    await db.commit()
    return None
    