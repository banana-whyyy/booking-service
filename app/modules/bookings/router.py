from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .services import create_booking_secure, get_booking_secure, get_multi_bookings_secure
from .schemas import BookingCreate, BookingResponse 
from .crud import delete_booking
from app.database import get_db
from ..auth.models import User
from app.dependencies import get_admin_user, get_current_user


router = APIRouter(tags=["bookings"], prefix="/bookings")


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def add_booking(
    booking: BookingCreate,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    new_booking = await create_booking_secure(db, booking, user_id)
    await db.commit()
    await db.refresh(new_booking)
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