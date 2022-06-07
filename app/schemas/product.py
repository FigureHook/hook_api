from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    size: Optional[int]
    scale: Optional[int]
    rerelease: bool
    adult: bool
    copyright: str
    url: str
    jan: Optional[str]
    order_period_start: Optional[datetime]
    order_period_end: Optional[datetime]


class Product(ProductBase):
    series: str
    category: str
    manufacturer: str
    releaser: Optional[str]
    distributer: Optional[str]
    sculptors: Optional[List[str]]
    paintworks: Optional[List[str]]
    official_images: List[str]


