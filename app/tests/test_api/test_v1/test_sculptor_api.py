import random

from app.tests.utils.worker import create_random_sculptor
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .util import v1_endpoint


def test_get_sculptors(db: Session, client: TestClient):
    worker_count = random.randint(0, 20)
    for _ in range(worker_count):
        create_random_sculptor(db)

    response = client.get(v1_endpoint('/sculptors'))
    assert response.status_code == 200

    content = response.json()
    assert type(content) is list
    assert len(content) == worker_count


def test_create_sculptor(db: Session, client: TestClient):
    data = {
        'name': "Master"
    }
    response = client.post(v1_endpoint('/sculptors/'), json=data)
    assert response.status_code == 201

    content = response.json()
    assert content.get('name') == data.get('name')

    response = client.post(v1_endpoint('/sculptors/'), json=data)
    assert response.status_code == 303
    assert 'Location' in response.headers
    assert f"/sculptors/{content.get('id')}" in response.headers['Location']


def test_get_sculptor(db: Session, client: TestClient):
    sculptor = create_random_sculptor(db)
    response = client.get(v1_endpoint(f'/sculptors/{sculptor.id}'))
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == sculptor.name

    response = client.get(v1_endpoint(f'/sculptors/1234235'))
    assert response.status_code == 404


def test_update_sculptor(db: Session, client: TestClient):
    sculptor = create_random_sculptor(db)
    update_data = {
        'name': "Another master"
    }
    response = client.put(v1_endpoint(
        f'/sculptors/{sculptor.id}'), json=update_data)
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == update_data.get('name')

    response = client.put(v1_endpoint(
        f'/sculptors/12341234'), json=update_data)
    assert response.status_code == 404


def test_delete_sculptor(db: Session, client: TestClient):
    sculptor = create_random_sculptor(db)
    response = client.delete(v1_endpoint(f'/sculptors/{sculptor.id}'))
    assert response.status_code == 204

    response = client.delete(v1_endpoint(f'/sculptors/{sculptor.id}'))
    assert response.status_code == 404
