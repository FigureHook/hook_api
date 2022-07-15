import random

from app.tests.utils.category import create_random_category
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_categories(db: Session, client: TestClient):
    categories_count = random.randint(0, 20)
    for _ in range(categories_count):
        create_random_category(db)

    response = client.get(v1_endpoint("/categories"))
    assert response.status_code == 200

    content = response.json()
    assert type(content) is list
    assert len(content) == categories_count
    for category in content:
        assert 'id' in category
        assert 'name' in category


def test_create_category(db: Session, client: TestClient):
    data = {
        'name': 'Doll'
    }

    response = client.post(v1_endpoint("/categories/"), json=data)
    assert response.status_code == 201

    content = response.json()
    assert 'id' in content
    assert 'name' in content
    assert content.get('name') == data.get('name')

    response = client.post(v1_endpoint("/categories/"), json=data)
    assert response.status_code == 303
    assert 'Location' in response.headers
    assert f"/categories/{content.get('id')}" in response.headers['Location']


def test_get_category(db: Session, client: TestClient):
    category = create_random_category(db)
    response = client.get(v1_endpoint(f"/categories/{category.id}"))
    assert response.status_code == 200

    content = response.json()
    for key in content:
        assert content.get(key) == getattr(category, key)


def test_update_category(db: Session, client: TestClient):
    category = create_random_category(db)
    update_data = {
        'name': "Doll"
    }
    response = client.put(
        v1_endpoint(f"/categories/{category.id}"),
        json=update_data
    )
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == update_data.get('name')

    response = client.put(
        v1_endpoint(f"/categories/1235345"),
        json=update_data
    )
    assert response.status_code == 404


def test_delete_category(db: Session, client: TestClient):
    category = create_random_category(db)
    response = client.delete(
        v1_endpoint(f"/categories/{category.id}")
    )
    assert response.status_code == 204

    response = client.delete(
        v1_endpoint(f"/categories/{category.id}")
    )
    assert response.status_code == 404
