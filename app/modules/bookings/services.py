from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import create_booking, delete_booking
from .schemas import BookingCreate
from .models import Booking
from modules.rooms.models import Room

async def create_booking_secure(db: AsyncSession, booking_data: BookingCreate, user_id: int):
    await db.execute(select(Room).where(Room.id == booking_data.room_id).with_for_update())
    intersects = await db.execute(
        select(Booking).where(
            Booking.room_id == booking_data.room_id,
            Booking.time_start < booking_data.time_end,
            Booking.time_end > booking_data.time_start
        )
    )

    if intersects.scalar() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time is already booked"
        )
    
    await create_booking(db, booking_data, user_id)

