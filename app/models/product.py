from datetime import date, datetime
from typing import Optional, Union, cast

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        SmallInteger, String)
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Mapped, relationship

from ..db.model_base import PkModel, PkModelWithTimestamps
from .category import Category
from .company import Company
from .relation_table import product_paintwork_table, product_sculptor_table
from .series import Series
from .worker import Paintwork, Sculptor

__all__ = [
    "ProductOfficialImage",
    "ProductReleaseInfo",
    "Product"
]


class ProductOfficialImage(PkModel):
    __tablename__ = "product_official_image"

    url: Mapped[str] = Column(String)
    order: Mapped[int] = Column(Integer)
    product_id: Mapped[int] = Column(Integer, ForeignKey(
        "product.id", ondelete="CASCADE"))

    @classmethod
    def create_image_list(cls, image_urls: list[str]) -> list['ProductOfficialImage']:
        images: list['ProductOfficialImage'] = []

        for url in image_urls:
            image = ProductOfficialImage(url=url)
            images.append(image)

        return images


class ProductReleaseInfo(PkModelWithTimestamps):
    __tablename__ = "product_release_info"

    price: Mapped[Optional[int]] = Column(Integer)
    tax_including: Mapped[bool] = Column(Boolean)
    initial_release_date: Mapped[Optional[date]] = Column(
        Date, nullable=True)  # type: ignore
    adjusted_release_date: Mapped[Optional[date]] = Column(Date)  # type: ignore
    announced_at: Mapped[Optional[date]] = Column(Date)
    shipped_at: Mapped[Optional[date]] = Column(Date)
    product_id: Mapped[int] = Column(Integer, ForeignKey(
        "product.id", ondelete="CASCADE"), nullable=False)
    product: Mapped['Product'] = relationship('Product', back_populates='release_infos')

    @property
    def release_date(self):
        return cast(Optional[date], self.adjusted_release_date or self.initial_release_date)

    def adjust_release_date_to(self, delay_date: Union[date, datetime, None]):
        if not delay_date:
            return self

        if isinstance(delay_date, datetime):
            delay_date = delay_date.date()

        assert isinstance(
            delay_date, date), f"{delay_date} must be `date` or `datetime`"

        has_init_release_date = bool(self.initial_release_date)

        if has_init_release_date:
            self.adjusted_release_date = delay_date  # type: ignore
        else:
            self.initial_release_date = delay_date  # type: ignore

        return self

    def stall(self):
        self.initial_release_date = None
        self.adjusted_release_date = None

        return self


class Product(PkModelWithTimestamps):
    """
    ## Column
    + checksum: MD5 value, one of methods to check the product should be updated.
    """
    __tablename__ = "product"

    # ---native columns---
    name: Mapped[str] = Column(String, nullable=False)  # type: ignore
    size: Mapped[int] = Column(SmallInteger)  # type: ignore
    scale: Mapped[int] = Column(SmallInteger)  # type: ignore
    rerelease: Mapped[bool] = Column(Boolean)  # type: ignore
    adult: Mapped[bool] = Column(Boolean)  # type: ignore
    copyright: Mapped[str] = Column(String)  # type: ignore
    url: Mapped[str] = Column(String)  # type: ignore
    jan: Mapped[str] = Column(String(13), unique=True)  # type: ignore
    id_by_official: Mapped[str] = Column(String)  # type: ignore
    checksum: Mapped[str] = Column(String(32))  # type: ignore
    order_period_start: Mapped[datetime] = Column(DateTime)  # type: ignore
    order_period_end: Mapped[datetime] = Column(DateTime)  # type: ignore
    thumbnail: Mapped[str] = Column(String)  # type: ignore
    og_image: Mapped[str] = Column(String)  # type: ignore

    # ---Foreign key columns---
    series_id: Mapped[int] = Column(Integer, ForeignKey("series.id"))
    series: Mapped[Series] = relationship(
        "Series",
        lazy="joined",
    )

    category_id: Mapped[int] = Column(Integer, ForeignKey("category.id"))
    category: Mapped[Category] = relationship(
        "Category",
        backref="products",
        lazy="joined",
    )

    manufacturer_id: Mapped[int] = Column(Integer, ForeignKey("company.id"))
    manufacturer: Mapped[Company] = relationship(
        "Company",
        backref="made_products",
        primaryjoin="Product.manufacturer_id == Company.id",
        lazy="joined"
    )

    releaser_id: Mapped[int] = Column(Integer, ForeignKey("company.id"))
    releaser: Mapped[Company] = relationship(
        "Company",
        backref="released_products",
        primaryjoin="Product.releaser_id == Company.id",
        lazy="joined"
    )

    distributer_id: Mapped[int] = Column(Integer, ForeignKey("company.id"))
    distributer: Mapped[Company] = relationship(
        "Company",
        backref="distributed_products",
        primaryjoin="Product.distributer_id == Company.id",
        lazy="joined"
    )

    # ---relationships field---
    release_infos: Mapped[list[ProductReleaseInfo]] = relationship(
        ProductReleaseInfo,
        back_populates="product",
        order_by="nulls_first(asc(ProductReleaseInfo.initial_release_date))",
        cascade="all, delete",
        passive_deletes=True,
        uselist=True
    )
    official_images: Mapped[list[ProductOfficialImage]] = relationship(
        ProductOfficialImage,
        backref="product",
        order_by="ProductOfficialImage.order",
        collection_class=ordering_list("order", count_from=1),
        cascade="all, delete",
        passive_deletes=True
    )
    sculptors: Mapped[list[Sculptor]] = relationship(
        "Sculptor",
        secondary=product_sculptor_table,
        backref="products",
        lazy="joined",
    )
    paintworks: Mapped[list[Paintwork]] = relationship(
        "Paintwork",
        secondary=product_paintwork_table,
        backref="products",
        lazy="joined",
    )

    @property
    def last_release(self) -> Union[ProductReleaseInfo, None]:
        return self.release_infos[-1] if self.release_infos else None

    def check_checksum(self, checksum: str) -> bool:
        return checksum == self.checksum
