import math
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

from .util import assert_pageination_content, v1_endpoint


def count_future_release(
    release_infos: Sequence[ProductReleaseInfo],
    from_: datetime,
    compare_announced_date: bool = True
) -> int:
    count = 0
    for info in release_infos:
        if info.created_at:
            if info.created_at >= from_:
                if compare_announced_date:
                    if info.announced_at:
                        if info.announced_at < from_:
                            continue

            count += 1

    return count


def test_get_multi_release_tickets(db: Session, client: TestClient):
    tickets = [
        create_random_release_ticket(db)
        for _ in range(random.randint(1, 10))
    ]
    tickets_count = len(tickets)
    results_size = random.randint(1, 20)
    expected_pages = math.ceil(
        tickets_count / results_size
    ) if tickets_count else 1
    expected_page = random.randint(1, expected_pages)
    response = client.get(
        url=v1_endpoint("/release-tickets"),
        params={
            'page': expected_page,
            'size': results_size
        }
    )
    assert response.status_code == 200

    content = response.json()
    assert_pageination_content(
        content=content,
        expected_page=expected_page,
        expected_pages=expected_pages,
        total_results=tickets_count,
        results_size=results_size
    )
    for result in content['results']:
        assert 'id' in result
        assert 'created_at' in result


def test_create_release_ticket(db: Session, client: TestClient):
    for _ in range(random.randint(1, 50)):
        product = create_random_product(db)
        for _ in range(random.randint(1, 3)):
            create_random_release_info_own_by_product(
                db, product_id=product.id)

    base_datetime = datetime.now()

    response = client.post(
        url=v1_endpoint("/release-tickets/"),
        json={
            'from': base_datetime.isoformat()
        }
    )
    assert response.status_code == 201

    content = response.json()
    assert 'id' in content


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
        url=v1_endpoint("/release-tickets/123")
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
