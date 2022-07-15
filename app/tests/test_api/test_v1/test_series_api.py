import random

from app.tests.utils.series import create_random_series
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_series_multi(db: Session, client: TestClient):
    series_count = random.randint(0, 5)
    for _ in range(series_count):
        create_random_series(db)

    response = client.get(v1_endpoint("/companys"))
    assert response.status_code == 200

    content = response.json()

    assert type(content) is list
    assert len(content) == series_count
    for seires in content:
        assert 'id' in seires
        assert 'name' in seires


def test_create_series(db: Session, client: TestClient):
    data = {
        'name': "Figure"
    }

    response = client.post(v1_endpoint("/series/"), json=data)
    assert response.status_code == 201

    content = response.json()
    for key in data:
        assert content.get(key) == data.get(key)

    response = client.post(v1_endpoint("/series/"), json=data)
    assert response.status_code == 303
    assert 'Location' in response.headers
    assert f"/series/{content.get('id')}" in response.headers['Location']


def test_get_series(db: Session, client: TestClient):
    series = create_random_series(db)

    response = client.get(v1_endpoint(f"/series/{series.id}"))
    assert response.status_code == 200
    content = response.json()
    for key in content:
        assert content.get(key) == getattr(series, key)


def test_update_series(db: Session, client: TestClient):
    series = create_random_series(db)
    update_data = {
        'name': "Doll"
    }
    response = client.put(
        v1_endpoint(f"/series/{series.id}"),
        json=update_data
    )
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == update_data.get('name')

    response = client.put(
        v1_endpoint("/series/887799988"),
        json=update_data
    )
    assert response.status_code == 404


def test_delete_series(db: Session, client: TestClient):
    series = create_random_series(db)
    response = client.delete(
        v1_endpoint(f"/series/{series.id}")
    )
    assert response.status_code == 204

    reposne = client.delete(
        v1_endpoint(f"/series{series.id}")
    )
    assert reposne.status_code == 404
