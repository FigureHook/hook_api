from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt


class ReleaseTicketCreate(BaseModel):
    from_: datetime = Field(..., alias='from')


class ReleaseTicketOut(BaseModel):
    release_ids: list[int]


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
    size: Optional[NonNegativeInt]
    scale: Optional[NonNegativeInt]
    price: Optional[NonNegativeInt]
    release_date: Optional[date]

    # Media
    image_url: str
    manufacturer_logo: Optional[str]