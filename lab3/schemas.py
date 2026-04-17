from pydantic import BaseModel
from typing import Optional

class HotelBase(BaseModel):
    name: str
    description: Optional[str] = None
    contactEmail: Optional[str] = None
    hotelChainId: Optional[int] = None

class HotelCreate(HotelBase):
    pass

class HotelResponse(HotelBase):
    hotelId: int

    class Config:
        from_attributes = True