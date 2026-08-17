from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from .crud import create_booking, get_booking
from .schemas import BookingCreate
from .models import Booking
from ..auth.models import User, UserRole
from ..rooms.schemas import RoomFilterParams
from ..rooms.models import Room


def get_time_intersection_conditions(time_start: datetime, time_end: datetime):
    return [Booking.time_start < time_end, Booking.time_end > time_start]


async def create_booking_secure(
    db: AsyncSession,
    booking_data: BookingCreate,
    user_id: int
) -> Booking:
    room = await db.execute(select(Room).where(Room.id == booking_data.room_id).with_for_update())
    if not room.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    conditions = get_time_intersection_conditions(booking_data.time_start, booking_data.time_end)
    intersects = await db.execute(
        select(Booking).where(
            Booking.room_id == booking_data.room_id,
            *conditions
        )
    )

    bonus_cost: int = 100
    if intersects.scalar() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time is already booked"
        )

    db_user_result = await db.execute(
        select(User).where(User.id == user_id).with_for_update()
    )
    db_user = db_user_result.scalar_one()

    if db_user.bonus_balance < bonus_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough bonuses",
        )

    db_user.bonus_balance -= bonus_cost
    
    return await create_booking(db, booking_data, db_user.id)


async def get_booking_secure(
    db: AsyncSession,
    booking_id: int,
    current_user: User,
):
    booking = await get_booking(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if current_user.id != booking.user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        ) 

    return booking


async def get_multi_bookings_secure(db: AsyncSession, current_user: User):
    stmt = select(Booking)

    if current_user.role != UserRole.ADMIN:
        stmt = stmt.where(current_user.id == Booking.user_id)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_available_rooms(db: AsyncSession, filters: RoomFilterParams) -> list[Room]:
    stmt = select(Room)

    if filters.time_start and filters.time_end:
        conditions = get_time_intersection_conditions(filters.time_start, filters.time_end)
        subquery = select(Booking).where(*conditions)
        stmt = stmt.where(Room.id.not_in(subquery))

    if filters.min_capacity is not None:
        stmt = stmt.where(Room.capacity >= filters.min_capacity)

    if filters.min_price is not None:
        stmt = stmt.where(Room.price_hour >= filters.min_price)

    if filters.max_price is not None:
        stmt = stmt.where(Room.price_hour <= filters.max_price)

    if filters.has_projector is not None:
        stmt = stmt.where(Room.has_projector == filters.has_projector)

    if filters.has_whiteboard is not None:
        stmt = stmt.where(Room.has_whiteboard == filters.has_whiteboard)
    
    stmt = stmt.offset(filters.offset).limit(filters.limit).order_by(Room.id)

    result = await db.scalars(stmt)
    return result.all()
