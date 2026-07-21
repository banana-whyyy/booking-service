from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from .models import Room
from .schemas import RoomCreate, RoomUpdate


async def create_room(db: AsyncSession, room: RoomCreate) -> Room:
    db_room = Room(**room.model_dump())
    db.add(db_room)
    await db.flush()
    return db_room


async def get_room(db: AsyncSession, room_id: int) -> Room | None:
    result = await db.execute(
        select(Room).where(Room.id == room_id)
    )
    return result.scalar_one_or_none()


async def get_room_by_name(db: AsyncSession, room_name: str) -> Room | None:
    result = await db.execute(select(Room).where(Room.name == room_name))
    return result.scalar_one_or_none()


async def room_update(db: AsyncSession, room_id: int, room_update: RoomUpdate) -> Room | None:
    db_room = await get_room(db, room_id)
    if not db_room:
        return None
    
    update_data = room_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)

    await db.flush()
    return db_room


async def room_delete(db: AsyncSession, room_id: int) -> bool:
    db_room = await get_room(db, room_id)
    if not db_room:
        return False
    
    await db.delete(db_room)
    await db.flush()
    return True