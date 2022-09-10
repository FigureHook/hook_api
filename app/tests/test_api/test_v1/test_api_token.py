from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.tests.utils.application import create_random_application
from app import crud

from .util import v1_endpoint


def test_unauth(db: Session, raw_client: TestClient):
    raw_client.headers["x-api-token"] = "kappa"
    response = raw_client.get(v1_endpoint("/products"))
    assert response.status_code == 401


def test_application_api_token(db: Session, raw_client: TestClient):
    app = create_random_application(db)
    raw_client.headers["x-api-token"] = app.token
    response = raw_client.get(v1_endpoint("/products"))
    assert response.status_code == 200

    db.refresh(app)
    seen_app = crud.application.get(db=db, id=app.id)
    assert seen_app
    assert seen_app.last_seen_at
