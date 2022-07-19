import random
from math import ceil

from app.tests.utils.category import create_random_category
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_categories(db: Session, client: TestClient):
    categories_count = random.randint(0, 20)
    results_size = random.randint(1, 100)
    expected_pages = ceil(
        categories_count / results_size
    ) if categories_count else 1
    expected_page = random.randint(1, expected_pages)
    for _ in range(categories_count):
        create_random_category(db)

    response = client.get(
        url=v1_endpoint("/categories"),
        params={
            'page': expected_page,
            'size': results_size
        }
    )
    assert response.status_code == 200

    content = response.json()
    assert 'page' in content
    assert 'total_pages' in content
    assert 'total_results' in content
    assert 'results' in content

    assert content.get('page') == expected_page
    assert content.get('total_pages') == expected_pages
    assert content.get('total_results') == categories_count

    assert type(content['results']) is list
    assert len(content['results']) <= results_size

    for category in content['results']:
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
