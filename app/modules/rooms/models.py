from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String
from datetime import datetime

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    price_hour: Mapped[int]
    capacity: Mapped[int] = mapped_column(default=5)
    has_projector: Mapped[bool]
    has_whiteboard: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

