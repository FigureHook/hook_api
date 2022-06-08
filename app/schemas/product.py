from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt, validator


class ProductOfficialImageBase(BaseModel):
    url: str
    order: NonNegativeInt = Field(
        default=0,
        title="The order of images.",
        description='''Specified the order of image.
        By default, 0 is for the last image.'''
    )


class ProductOfficialImageCreate(ProductOfficialImageBase):
    pass


class ProductOfficialImageUpdate(ProductOfficialImageBase):
    pass


class ProductBase(BaseModel):
    name: str
    size: Optional[PositiveInt]
    scale: Optional[PositiveInt]
    rerelease: bool
    adult: bool = Field(default=False)
    copyright: str
    url: str
    jan: Optional[str]
    checksum: str
    order_period_start: Optional[datetime] = Field(
        title="The begining of order period.",
        description="This value should be an UTC timestamp."
    )
    order_period_end: Optional[datetime] = Field(
        title="The end of order period.",
        description="This value should be an UTC timestamp."
    )
    series: str
    category: str
    manufacturer: str
    releaser: Optional[str]
    distributer: Optional[str]
    sculptors: Optional[list[str]]
    paintworks: Optional[list[str]]

    @validator('jan')
    def validate_jan(cls, jan_v: str) -> str:
        assert len(jan_v) == 13
        assert jan_v.isnumeric()
        assert _validate_jan(jan_v)
        return jan_v


def _validate_jan(s):
    return not sum(int(i)*d for i, d in zip(s, [1, 3]*7)) % 10


class ProductCreate(ProductBase):
    official_images: list[str]


class ProductUpdate(ProductBase):
    pass
