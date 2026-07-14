from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal



class RoomCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    price_hour: Decimal = Field(gt=0)
    capacity: int = Field(ge=1)
    has_projector: bool = False
    has_whiteboard: bool = False

class RoomResponse(RoomCreate):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class RoomUpdate(BaseModel): 
    name: str | None = None
    description: str | None = None
    price_hour: Decimal | None = None 
    capacity: int | None = None
    has_projector: bool | None = None
    has_whiteboard: bool | None = None