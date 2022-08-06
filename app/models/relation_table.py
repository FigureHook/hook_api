from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from ..db.model_base import Model

metadata = Model.metadata
# association table
product_sculptor_table = Table(
    "product_sculptor", metadata,
    Column("product_id", Integer, ForeignKey(
        "product.id", ondelete="CASCADE")),
    Column("sculptor_id", Integer, ForeignKey(
        "sculptor.id", ondelete="CASCADE"))
)

product_paintwork_table = Table(
    "product_paintwork", metadata,
    Column("product_id", Integer, ForeignKey(
        "product.id", ondelete="CASCADE")),
    Column("paintwork_id", Integer, ForeignKey(
        "paintwork.id", ondelete="CASCADE"))
)


feed_ticket_release_table = Table(
    "release_ticket_release_info_rel", metadata,
    Column('ticket_id', UUID(as_uuid=True), ForeignKey(
        'release_ticket.id', ondelete="CASCADE")),
    Column('release_info_id', Integer, ForeignKey(
        'product_release_info.id', ondelete="CASCADE")),
)
