from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, validator


class ProductReleaseInfoBase(BaseModel):
    price: Optional[NonNegativeInt]
    tax_including: bool = Field(default=False)
    initial_release_date: Optional[date]
    adjusted_release_date: Optional[date]
    announced_at: Optional[date]
    shipped_at: Optional[date]


class ProductReleaseInfoCreate(ProductReleaseInfoBase):
    pass


class ProductReleaseInfoUpdate(ProductReleaseInfoBase):
    pass
