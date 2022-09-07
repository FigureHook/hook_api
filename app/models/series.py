from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, Query, relationship
from .product import Product

from ..db.model_base import PkModel, UniqueMixin

__all__ = ["Series"]


class Series(UniqueMixin, PkModel):
    __tablename__ = "series"

    name: Mapped[str] = Column(String, unique=True)  # type: ignore
    products: Mapped[list[Product]] = relationship('Product', uselist=True)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query: Query, *args, **kwargs):
        return query.filter(Series.name == kwargs.get('name'))
