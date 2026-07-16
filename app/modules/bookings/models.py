from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

from app.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.rooms.models import Room


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    time_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    time_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    status: Mapped[BookingStatus] = mapped_column(default=BookingStatus.PENDING)
    room: Mapped["Room"] = relationship(back_populates="bookings", lazy="joined")
