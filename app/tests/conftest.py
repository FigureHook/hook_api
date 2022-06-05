from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import pgsql_db
from app.db.base import Model
from app.core.config import settings
import pytest
import psycopg2
import os
from typing import Dict, Generator

os.environ['ENV'] = "test"


def check_test_database():
    connection = None

    try:
        connection = psycopg2.connect(
            f"user={settings.POSTGRES_USER} host={settings.POSTGRES_SERVER} password={settings.POSTGRES_PASSWORD} port='5432'")

    except:
        print('Database not connected.')

    if connection is not None:
        connection.autocommit = True

        cur = connection.cursor()
        cur.execute(f"SELECT datname FROM pg_database;")

        list_database = cur.fetchall()
        database_name = settings.POSTGRES_DB

        if (database_name,) not in list_database:
            sql = f"CREATE database {database_name};"
            cur.execute(sql)

        connection.close()


@pytest.fixture(scope="function")
def db() -> Generator:
    check_test_database()
    Model.metadata.create_all(bind=pgsql_db.engine)
    session = pgsql_db.Session()

    yield session

    session.close()
    Model.metadata.drop_all(bind=pgsql_db.engine)
