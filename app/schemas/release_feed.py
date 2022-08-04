from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt


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
    og_image: Optional[str]
    manufacturer_logo: Optional[str]

    @property
    def media_image(self):
        return self.og_image if self.og_image else self.image_url
