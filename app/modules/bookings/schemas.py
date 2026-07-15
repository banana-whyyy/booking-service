from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timedelta
from typing import Self

from .models import BookingStatus
from rooms.schemas import RoomResponse


class BookingBase(BaseModel):
    room_id: int 
    time_start: datetime 
    time_end: datetime
    @model_validator(mode="after")
    def validate_booking_items(self) -> Self:
        if (self.time_end < self.time_start):
            raise ValueError(
                f"Invalid interval: time start ({self.time_end}) "
                f"must be later than start time({self.time_start})"
            )
        
        duration = self.time_end - self.time_start

        if duration < timedelta(minutes=30) or duration > timedelta(hours=12):
            raise ValueError(
                f"The level duration must be no less than " 
                f"30 minutes and no more than 12 hours."
            )
        return self
        

class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    user_id: int
    status: BookingStatus
    room: RoomResponse
