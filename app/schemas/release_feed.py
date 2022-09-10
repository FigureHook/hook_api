from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt


class ReleaseTicketCreate(BaseModel):
    from_: datetime = Field(..., alias="from")


class ReleaseTicketInDB(BaseModel):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


class ReleaseFeed(BaseModel):
    # Metadata
    product_id: int
    release_info_id: int
    name: str
    source_url: str
    is_nsfw: bool
    is_rerelease: bool
    series: str
    manufacturer: str
    size: Optional[NonNegativeInt] = Field(nullable=True)
    scale: Optional[NonNegativeInt] = Field(nullable=True)
    price: Optional[NonNegativeInt] = Field(nullable=True)
    release_date: Optional[date] = Field(nullable=True)

    # Media
    image_url: str
    manufacturer_logo: Optional[str] = Field(nullable=True)
