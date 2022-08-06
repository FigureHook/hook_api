import random
import uuid
from datetime import datetime
from typing import Sequence

from app.models import ProductReleaseInfo
from app.tests.utils.product import create_random_product
from app.tests.utils.release_info import \
    create_random_release_info_own_by_product
from app.tests.utils.release_ticket import create_random_release_ticket
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def count_future_release(
    release_infos: Sequence[ProductReleaseInfo],
    from_: datetime,
    compare_announced_date: bool = True
) -> int:
    count = 0
    for info in release_infos:
        if info.created_at >= from_:
            if compare_announced_date:
                if info.announced_at < from_:
                    continue

            count += 1

    return count


def test_create_release_ticket(db: Session, client: TestClient):
    products = [
        create_random_product(db)
        for _ in range(random.randint(1, 50))
    ]
    release_infos = [
        create_random_release_info_own_by_product(db, product_id=p.id)
        for _ in range(random.randint(1, 3))
        for p in products
    ]

    base_datetime = datetime.now()
    expected_count = count_future_release(
        release_infos=release_infos,
        from_=base_datetime
    )

    response = client.post(
        url=v1_endpoint("/release-tickets/"),
        json={
            'from': base_datetime.isoformat()
        }
    )
    assert response.status_code == 201

    content = response.json()
    assert 'release_ids' in content
    assert len(content['release_ids']) == expected_count


def test_get_release_ticket(db: Session, client: TestClient):
    ticket = create_random_release_ticket(db)
    assert type(ticket.id) is uuid.UUID
    ticket_uid = uuid.UUID(str(ticket.id))
    response = client.get(
        url=v1_endpoint(f"/release-tickets/{ticket_uid.hex}"),
        params={
            'type': 'feed'
        }
    )
    assert response.status_code == 200

    response = client.get(
        url=v1_endpoint(f"/release-tickets/{uuid.uuid4().hex}")
    )
    assert response.status_code == 404

    response = client.get(
        url=v1_endpoint(f"/release-tickets/123")
    )
    assert response.status_code == 404


def test_delete_release_ticket(db: Session, client: TestClient):
    ticket = create_random_release_ticket(db)
    assert type(ticket.id) is uuid.UUID
    ticket_uid = uuid.UUID(str(ticket.id))
    response = client.delete(
        url=v1_endpoint(f"/release-tickets/{ticket_uid.hex}")
    )
    assert response.status_code == 204

    response = client.get(
        url=v1_endpoint(f"/release-tickets/{ticket_uid.hex}")
    )
    assert response.status_code == 404
