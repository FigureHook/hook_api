import os
from typing import Generator

import pytest

os.environ["ENV"] = "test"

if os.environ["ENV"] == "test":
    import psycopg2
    from app.core.config import settings
    from app.db.base import Model
    from app.db.session import pgsql_db
    from app.main import app
    from fastapi.testclient import TestClient
else:
    raise ValueError


def check_test_database():

    connection = None

    try:
        connection = psycopg2.connect(
            host=settings.POSTGRES_SERVER,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
        )

    except:  # noqa: E722
        print("Database not connected.")

    if connection is not None:
        connection.autocommit = True

        cur = connection.cursor()
        cur.execute("SELECT datname FROM pg_database;")

        list_database = cur.fetchall()
        database_name = settings.POSTGRES_DB

        if (database_name,) not in list_database:
            sql = f"CREATE database {database_name};"
            cur.execute(sql)

        connection.close()


@pytest.fixture(scope="module")
def raw_client() -> Generator:
    check_test_database()
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def client(raw_client: TestClient) -> Generator:
    raw_client.headers["x-api-token"] = settings.API_TOKEN
    yield raw_client


@pytest.fixture(scope="function")
def db() -> Generator:
    check_test_database()
    Model.metadata.create_all(bind=pgsql_db.engine)
    session = pgsql_db.Session()

    yield session

    session.close()
    Model.metadata.drop_all(bind=pgsql_db.engine)
