from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Booking
from .schemas import BookingCreate
from ..auth.models import User


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


async def delete_booking(db: AsyncSession, booking_id: int, user: User) -> bool:
    stmt = delete(Booking).where(Booking.id == booking_id)

    if user.role != "admin":
        stmt = stmt.where(Booking.user_id == user.id)

    stmt = stmt.returning(Booking.id)
    result = await db.execute(stmt)
    deleted_it = result.scalar_one_or_none()

    return deleted_it is not None