from datetime import date, datetime
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


class ProductReleaseInfoInDB(ProductReleaseInfoBase):
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
