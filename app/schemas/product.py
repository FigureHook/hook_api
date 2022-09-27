from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt, validator

from .category import CategoryInDB
from .company import CompanyInDB
from .series import SeriesInDB
from .worker import WorkerInDB


class ProductOfficialImageBase(BaseModel):
    url: str


class ProductOfficialImageCreate(ProductOfficialImageBase):
    pass


class ProductOfficialImageUpdate(ProductOfficialImageBase):
    order: NonNegativeInt = Field(
        default=0,
        title="The order of images.",
        description="Specified the order of image."
        "By default, 0 is for the last image.",
    )


class ProductOfficialImageInDB(ProductOfficialImageBase):
    id: int

    class Config:
        orm_mode = True


class ProductRequiredMeta(BaseModel):
    name: str
    manufacturer: str
    category: str
    url: str
    checksum: str
    rerelease: bool
    adult: bool = Field(default=False)


class ProductOptionalMeta(BaseModel):
    size: Optional[PositiveInt] = Field(nullable=True)
    scale: Optional[PositiveInt] = Field(nullable=True)

    order_period_start: Optional[datetime] = Field(
        title="The begining of order period.",
        description="This value should be an UTC timestamp.",
        nullable=True,
    )
    order_period_end: Optional[datetime] = Field(
        title="The end of order period.",
        description="This value should be an UTC timestamp.",
        nullable=True,
    )

    series: Optional[str]
    copyright: Optional[str]
    jan: Optional[str]
    releaser: Optional[str] = Field(nullable=True)
    distributer: Optional[str] = Field(nullable=True)
    sculptors: Optional[list[str]] = []
    paintworks: Optional[list[str]] = []


class ProductBase(ProductOptionalMeta, ProductRequiredMeta):
    @validator("jan")
    def validate_jan(cls, jan_v: Optional[str]) -> Optional[str]:
        if jan_v:
            assert len(jan_v) == 13
            assert jan_v.isnumeric()
            assert _validate_jan(jan_v)
        return jan_v


def _validate_jan(s):
    return not sum(int(i) * d for i, d in zip(s, [1, 3] * 7)) % 10


class ProductCreate(ProductBase):
    official_images: list[str]


class ProductUpdate(ProductBase):
    pass


class ProductInDB(BaseModel):
    id: int
    name: str
    size: Optional[PositiveInt] = Field(nullable=True)
    scale: Optional[PositiveInt] = Field(nullable=True)
    rerelease: bool
    adult: bool = Field(default=False)
    copyright: Optional[str]
    url: str
    jan: Optional[str] = Field(nullable=True)
    checksum: str
    order_period_start: Optional[datetime] = Field(
        title="The begining of order period.",
        description="This value should be an UTC timestamp.",
        nullable=True,
    )
    order_period_end: Optional[datetime] = Field(
        title="The end of order period.",
        description="This value should be an UTC timestamp.",
        nullable=True,
    )

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductInDBRich(ProductInDB):
    series: SeriesInDB
    category: CategoryInDB
    manufacturer: CompanyInDB
    releaser: Optional[CompanyInDB] = Field(nullable=True)
    distributer: Optional[CompanyInDB] = Field(nullable=True)
    sculptors: Optional[list[WorkerInDB]] = []
    paintworks: Optional[list[WorkerInDB]] = []
    official_images: list[ProductOfficialImageInDB]
