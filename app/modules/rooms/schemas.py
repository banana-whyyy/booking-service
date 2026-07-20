from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class RoomBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    price_hour: Decimal = Field(ge=0)
    capacity: int = Field(ge=1)
    has_projector: bool = False
    has_whiteboard: bool = False


class RoomCreate(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class RoomUpdate(BaseModel): 
    name: str | None = None
    description: str | None = None
    price_hour: Decimal | None = Field(None, ge=0) 
    capacity: int | None = None
    has_projector: bool | None = None
    has_whiteboard: bool | None = None


class RoomFilterParams(BaseModel):
    time_start: datetime | None = None
    time_end: datetime | None = None

    min_capacity: int | None = Field(None, ge=1)
    min_price: Decimal | None = Field(None, ge=0)
    max_price: Decimal | None = Field(None, ge=0)

    has_projector: bool | None = None
    has_whiteboard: bool | None = None

    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)