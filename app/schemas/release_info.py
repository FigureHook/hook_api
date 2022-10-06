from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt


class ProductReleaseInfoBase(BaseModel):
    price: Optional[NonNegativeInt] = Field(nullable=True)
    tax_including: Optional[bool] = Field(nullable=True)
    initial_release_date: Optional[date] = Field(nullable=True)
    adjusted_release_date: Optional[date] = Field(nullable=True)
    announced_at: Optional[date] = Field(nullable=True)
    shipped_at: Optional[date] = Field(nullable=True)


class ProductReleaseInfoCreate(ProductReleaseInfoBase):
    tax_including: bool = Field(default=False)
    pass


class ProductReleaseInfoUpdate(ProductReleaseInfoBase):
    pass


class ProductReleaseInfoInDB(ProductReleaseInfoBase):
    tax_including: bool = Field(default=False)

    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
