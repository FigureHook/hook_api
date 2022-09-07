from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, Query
from ..db.model_base import PkModel, UniqueMixin

__all__ = ["Category"]


class Category(UniqueMixin, PkModel):
    __tablename__ = "category"

    name: Mapped[str] = Column(
        String, nullable=False, unique=True)  # type: ignore

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query: Query, *args, **kwargs):
        return query.filter(Category.name == kwargs.get('name'))
