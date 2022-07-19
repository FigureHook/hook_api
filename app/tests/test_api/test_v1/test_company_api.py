import random
from math import ceil

from app.tests.utils.company import create_random_company
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_companies(db: Session, client: TestClient):
    company_count = random.randint(0, 20)
    results_size = random.randint(1, 100)
    expected_pages = ceil(
        company_count / results_size
    ) if company_count else 1
    expected_page = random.randint(1, expected_pages)
    for _ in range(company_count):
        create_random_company(db)

    response = client.get(v1_endpoint("/companies"))
    assert response.status_code == 200

    content = response.json()
    assert 'page' in content
    assert 'total_pages' in content
    assert 'total_results' in content
    assert 'results' in content

    assert content.get('page') == expected_page
    assert content.get('total_pages') == expected_pages
    assert content.get('total_results') == company_count

    assert type(content['results']) is list
    assert len(content['results']) <= results_size
    for company in content['results']:
        assert 'id' in company
        assert 'name' in company


def test_create_company(db: Session, client: TestClient):
    data = {
        'name': "GSC"
    }

    response = client.post(v1_endpoint("/companies/"), json=data)
    assert response.status_code == 201

    content = response.json()
    for key in data:
        assert content.get(key) == data.get(key)

    response = client.post(v1_endpoint("/companies/"), json=data)
    assert response.status_code == 303
    assert 'Location' in response.headers
    assert f"/companies/{content.get('id')}" in response.headers['Location']


def test_get_company(db: Session, client: TestClient):
    company = create_random_company(db)

    response = client.get(v1_endpoint(f"/companies/{company.id}"))
    assert response.status_code == 200
    content = response.json()
    for key in content:
        assert content.get(key) == getattr(company, key)


def test_update_company(db: Session, client: TestClient):
    company = create_random_company(db)
    update_data = {
        'name': "GoodSmileCompany"
    }
    response = client.put(
        v1_endpoint(f"/companies/{company.id}"),
        json=update_data
    )
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == update_data.get('name')

    response = client.put(
        v1_endpoint("/companies/887799988"),
        json=update_data
    )
    assert response.status_code == 404


def test_delete_company(db: Session, client: TestClient):
    company = create_random_company(db)
    response = client.delete(
        v1_endpoint(f"/companies/{company.id}")
    )
    assert response.status_code == 204

    reposne = client.delete(
        v1_endpoint(f"/companies{company.id}")
    )
    assert reposne.status_code == 404
