from uuid import UUID

import pytest
from app.models import ReleaseTicket
from app.tests.utils.product import create_random_product
from app.tests.utils.release_info import create_random_release_info_own_by_product
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestReleaseTicket:
    def test_ticket_attribute(self, db: Session):
        product = create_random_product(db)
        release_info = create_random_release_info_own_by_product(
            db, product_id=product.id
        )
        ticket = ReleaseTicket(release_infos=[release_info])
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        assert type(ticket.id) is UUID
