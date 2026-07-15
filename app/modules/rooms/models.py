from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, DateTime, func, Numeric
from datetime import datetime
from decimal import Decimal

from app.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.bookings.models import Booking


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    price_hour: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    capacity: Mapped[int] = mapped_column(default=5)
    has_projector: Mapped[bool]
    has_whiteboard: Mapped[bool]

    bookings: Mapped[list["Booking"]] = relationship(back_populates="room", lazy="selectin")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

