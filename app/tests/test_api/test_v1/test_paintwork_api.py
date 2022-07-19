import random
from math import ceil

from app.tests.utils.worker import create_random_paintwork
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import assert_pageination_content, v1_endpoint


def test_get_paintworks(db: Session, client: TestClient):
    worker_count = random.randint(0, 20)
    results_size = random.randint(1, 100)
    expected_pages = ceil(
        worker_count / results_size
    ) if worker_count else 1
    expected_page = random.randint(1, expected_pages)
    for _ in range(worker_count):
        create_random_paintwork(db)

    response = client.get(
        url=v1_endpoint('/paintworks'),
        params={
            'page': expected_page,
            'size': results_size
        }
    )
    assert response.status_code == 200

    content = response.json()
    assert_pageination_content(
        content,
        expected_page=expected_page,
        expected_pages=expected_pages,
        total_results=worker_count,
        results_size=results_size
    )


def test_create_paintwork(db: Session, client: TestClient):
    data = {
        'name': "Master"
    }
    response = client.post(v1_endpoint('/paintworks/'), json=data)
    assert response.status_code == 201

    content = response.json()
    assert content.get('name') == data.get('name')

    response = client.post(v1_endpoint('/paintworks/'), json=data)
    assert response.status_code == 303
    assert 'Location' in response.headers
    assert f"/paintworks/{content.get('id')}" in response.headers['Location']


def test_get_paintwork(db: Session, client: TestClient):
    paintwork = create_random_paintwork(db)
    response = client.get(v1_endpoint(f'/paintworks/{paintwork.id}'))
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == paintwork.name

    response = client.get(v1_endpoint(f'/paintworks/1234235'))
    assert response.status_code == 404


def test_update_paintwork(db: Session, client: TestClient):
    paintwork = create_random_paintwork(db)
    update_data = {
        'name': "Another master"
    }
    response = client.put(
        v1_endpoint(f'/paintworks/{paintwork.id}'),
        json=update_data)
    assert response.status_code == 200

    content = response.json()
    assert content.get('name') == update_data.get('name')

    response = client.put(
        v1_endpoint(f'/paintworks/12341234'),
        json=update_data)
    assert response.status_code == 404


def test_delete_paintwork(db: Session, client: TestClient):
    paintwork = create_random_paintwork(db)
    response = client.delete(v1_endpoint(f'/paintworks/{paintwork.id}'))
    assert response.status_code == 204

    response = client.delete(v1_endpoint(f'/paintworks/{paintwork.id}'))
    assert response.status_code == 404
