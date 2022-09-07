import random
from datetime import datetime
from typing import Optional

from app.models import ProductReleaseInfo, ReleaseTicket
from app.tests.utils.faker import faker
from sqlalchemy import select
from sqlalchemy.orm import Session

from .product import create_random_product
from .release_info import create_random_release_info_own_by_product

__all__ = (
    'create_random_release_ticket',
)


def create_random_release_ticket(
    db: Session,
    from_datetime: Optional[datetime] = None,
    create_product: bool = True
) -> ReleaseTicket:
    if not from_datetime:
        from_datetime = faker.past_datetime()

    if create_product:
        for _ in range(random.randint(1, 50)):
            product = create_random_product(db)
            for _ in range(random.randint(1, 3)):
                create_random_release_info_own_by_product(
                    db, product_id=product.id)

    stmt = select(ProductReleaseInfo).filter(
        ProductReleaseInfo.announced_at is not None,
        ProductReleaseInfo.announced_at > from_datetime,
        ProductReleaseInfo.created_at >= from_datetime,
    )
    future_releases = db.scalars(stmt).unique().all()
    ticket = ReleaseTicket()
    ticket.release_infos = future_releases
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
