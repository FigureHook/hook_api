import random

from app.tests.utils.company import create_random_company
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_companys(db: Session, client: TestClient):
    company_count = random.randint(0, 20)
    for _ in range(company_count):
        create_random_company(db)

    response = client.get(v1_endpoint("/companys"))
    assert response.status_code == 200

    content = response.json()

    assert type(content) is list
    assert len(content) == company_count
    for company in content:
        assert 'id' in company
        assert 'name' in company


def test_create_company(db: Session, client: TestClient):
    data = {
        'name': "GSC"
    }

    response = client.post(v1_endpoint("/companys/"), json=data)
    assert response.status_code == 201

    content = response.json()
    for key in data:
        assert content.get(key) == data.get(key)

    response = client.post(v1_endpoint("/companys/"), json=data)
    assert response.status_code == 303
    assert 'Location' in response.headers
    assert f"/companys/{content.get('id')}" in response.headers['Location']


def test_get_company(db: Session, client: TestClient):
    company = create_random_company(db)

    response = client.get(v1_endpoint(f"/companys/{company.id}"))
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
        v1_endpoint(f"/companys/{company.id}"),
        json=update_data
    )
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == update_data.get('name')

    response = client.put(
        v1_endpoint("/companys/887799988"),
        json=update_data
    )
    assert response.status_code == 404


def test_delete_company(db: Session, client: TestClient):
    company = create_random_company(db)
    response = client.delete(
        v1_endpoint(f"/companys/{company.id}")
    )
    assert response.status_code == 204

    reposne = client.delete(
        v1_endpoint(f"/companys{company.id}")
    )
    assert reposne.status_code == 404
