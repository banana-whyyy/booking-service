from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Booking
from .schemas import BookingCreate


async def create_booking(db: AsyncSession, booking_data: BookingCreate, user_id: int) -> Booking:
    booking = Booking(**booking_data.model_dump(), user_id=user_id)
    await db.add(booking)
    await db.flush()
    return booking


async def get_booking(db: AsyncSession, booking_id: int, user_id: int) -> Booking | None:
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_bookings(db: AsyncSession, user_id: int) -> list[Booking]:
    result = await db.scalars(
        select(Booking).where(Booking.user_id == user_id)
    )
    return list(result.all())


async def delete_booking(db: AsyncSession, booking_id: int, user_id: int) -> bool:
    db_booking = await get_booking(db, booking_id, user_id)
    if db_booking is None: 
        return False

    await db.delete(db_booking)
    await db.flush()
    return True