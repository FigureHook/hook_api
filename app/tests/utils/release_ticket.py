import random

from app.models import ReleaseTicket
from sqlalchemy.orm import Session

from .product import create_random_product
from .release_info import create_random_release_info_own_by_product


__all__ = (
    'create_random_release_ticket',
)


def create_random_release_ticket(db: Session) -> ReleaseTicket:
    products = [
        create_random_product(db)
        for _ in range(random.randint(1, 50))
    ]
    release_infos = [
        create_random_release_info_own_by_product(db, product_id=p.id)
        for _ in range(random.randint(1, 3))
        for p in products
    ]

    ticket = ReleaseTicket(release_infos=release_infos)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
