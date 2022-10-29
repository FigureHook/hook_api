from typing import TYPE_CHECKING

from app.db.model_base import UUIDPkModel
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, Column

from .relation_table import feed_ticket_release_table

if TYPE_CHECKING:
    from .product import ProductReleaseInfo

__all__ = ("ReleaseTicket",)


class ReleaseTicket(UUIDPkModel):
    __tablename__ = "release_ticket"

    purpose: Mapped[str] = Column(String)  # type: ignore
    release_infos: Mapped[list["ProductReleaseInfo"]] = relationship(
        "ProductReleaseInfo",
        secondary=feed_ticket_release_table,
        backref="tickets",
        lazy="joined",
    )  # type: ignore
