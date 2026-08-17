from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .services import create_booking_secure, get_booking_secure, get_multi_bookings_secure
from .schemas import BookingCreate, BookingResponse 
from .crud import delete_booking
from app.database import get_db
from ..auth.models import User
from app.dependencies import get_current_user
from ..notifications.tasks import process_booking_notification


router = APIRouter(tags=["bookings"], prefix="/bookings")


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def add_booking(
    booking: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_booking = await create_booking_secure(db, booking, current_user.id)
    await db.commit()
    await db.refresh(new_booking)
    notification_payload = {
        "booking_id": new_booking.id,
        "username": current_user.username, 
        "user_email": current_user.email,
        "room_name": getattr(new_booking.room, "name", f"Room #{new_booking.room_id}"),
        "time_start": new_booking.time_start.isoformat(),
        "time_end": new_booking.time_end.isoformat(),
    }

    process_booking_notification.delay(notification_payload)

    return new_booking


@router.get("", response_model=list[BookingResponse])
async def read_bookings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_multi_bookings_secure(db, current_user)


@router.get("/{booking_id}", response_model=BookingResponse)
async def read_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_booking_secure(db, booking_id, current_user)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await delete_booking(db, booking_id, current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found or access denied",
        )
    await db.commit()
    return None