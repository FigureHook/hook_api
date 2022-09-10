import random

from app.tests.utils.application import create_random_application
from app.tests.utils.faker import faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_applications(db: Session, client: TestClient):
    application_count = random.randint(0, 10)
    for _ in range(application_count):
        create_random_application(db)
    response = client.get(v1_endpoint("/applications"))
    assert response.status_code == 200

    content = response.json()
    assert type(content) is list
    assert len(content) is application_count


def test_create_application(db: Session, client: TestClient):
    data = {"name": faker.slug()}
    response = client.post(v1_endpoint("/applications/"), json=data)
    assert response.status_code == 201

    content = response.json()
    assert content.get("name") == data.get("name")


def test_get_application(db: Session, client: TestClient):
    app = create_random_application(db)
    response = client.get(v1_endpoint(f"/applications/{app.id}"))
    assert response.status_code == 200

    content = response.json()
    assert str(getattr(app, "id")) == content.get("id")
    assert getattr(app, "name") == content.get("name")
    assert getattr(app, "token") == content.get("token")

    response = client.get(v1_endpoint(f"/applications/{faker.uuid4()}"))
    assert response.status_code == 404


def test_delete_application(db: Session, client: TestClient):
    app = create_random_application(db)
    response = client.delete(v1_endpoint(f"/applications/{app.id}"))
    assert response.status_code == 204

    response = client.delete(v1_endpoint(f"/applications/{faker.uuid4()}"))
    assert response.status_code == 404


def test_refresh_application_token(db: Session, client: TestClient):
    app = create_random_application(db)
    original_token = app.token
    response = client.post(v1_endpoint(f"/applications/{app.id}/refresh"))
    assert response.status_code == 200

    content = response.json()
    assert content["token"] != original_token

    response = client.post(v1_endpoint(f"/applications/{faker.uuid4()}/refresh"))
    assert response.status_code == 404
