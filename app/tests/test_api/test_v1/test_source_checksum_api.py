import random
from datetime import datetime
from typing import cast

from app.tests.utils.faker import faker
from app.tests.utils.source_checksum import create_random_source_checksum
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_source_checksums(db: Session, client: TestClient):
    checksum_count = random.randint(0, 5)
    for _ in range(checksum_count):
        create_random_source_checksum(db)

    response = client.get(v1_endpoint("/source-checksums"))
    assert response.status_code == 200

    content = response.json()
    assert type(content) is list
    assert len(content) is checksum_count


def test_create_source_checksum(db: Session, client: TestClient):
    data = {
        "source": faker.company(),
        "checksum": faker.hexify("^^^^^^^^^^^^^^^^^^"),
        "checked_at": faker.iso8601(),
    }

    response = client.post(v1_endpoint("/source-checksums/"), json=data)
    assert response.status_code == 201

    content = response.json()
    for key in data:
        assert data.get(key) == content.get(key)

    response = client.post(v1_endpoint("/source-checksums/"), json=data)
    assert response.status_code == 303
    assert "Location" in response.headers
    assert f"/source-checksums/{content.get('id')}" in response.headers["Location"]


def test_get_source_checksum(db: Session, client: TestClient):
    source_checksum = create_random_source_checksum(db)
    response = client.get(v1_endpoint(f"/source-checksums/{source_checksum.id}"))
    assert response.status_code == 200

    content = response.json()
    for key in content:
        orm_attr = getattr(source_checksum, key)
        if type(orm_attr) is datetime:
            orm_attr = orm_attr.isoformat()
        assert content.get(key) == orm_attr

    response = client.get(v1_endpoint("/source-checksums/123541"))
    assert response.status_code == 404


def test_update_source_checksum(db: Session, client: TestClient):
    source_checksum = create_random_source_checksum(db)
    udpate_data = {
        "checksum": faker.hexify("^^^^^^^^^^^^^^^^^^"),
        "checked_at": faker.iso8601(),
    }
    response = client.patch(
        url=v1_endpoint(f"/source-checksums/{source_checksum.id}"), json=udpate_data
    )
    assert response.status_code == 200

    content = response.json()
    for key in udpate_data:
        assert udpate_data.get(key) == content.get(key)

    response = client.patch(
        url=v1_endpoint("/source-checksums/938722"), json=udpate_data
    )
    assert response.status_code == 404


def test_delete_source_checksum(db: Session, client: TestClient):
    source_checksum = create_random_source_checksum(db)
    response = client.delete(v1_endpoint(f"/source-checksums/{source_checksum.id}"))
    assert response.status_code == 204

    response = client.delete(v1_endpoint("/source-checksums/838828"))
    assert response.status_code == 404


def test_get_source_checksums_by_name(db: Session, client: TestClient):
    source_checksums = [create_random_source_checksum(db) for _ in range(10)]
    for sc in source_checksums:
        response = client.get(
            v1_endpoint("/source-checksums"), params={"source": cast(str, sc.source)}
        )
        assert response.status_code == 200
        content = response.json()
        assert len(content)
        assert len(content) <= len(source_checksums)
