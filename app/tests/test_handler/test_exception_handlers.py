from app.main import app
from fastapi.testclient import TestClient


def test_sqlalchemy_exception_handler():
    from sqlalchemy.exc import SQLAlchemyError

    async def fake_endpoint():
        raise SQLAlchemyError('A SqlAlchemyError.')

    error_endpoint = '/sqlalchemy-error'
    app.add_api_route(error_endpoint, fake_endpoint, methods=['GET'])

    with TestClient(app) as client:
        response = client.get(error_endpoint)
        assert response.status_code == 500

        content = response.content
        assert content
        assert b"Internal server error." in content
