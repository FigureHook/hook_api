import random

from app.tests.utils.webhook import create_random_webhook
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import v1_endpoint


def test_get_webhooks(db: Session, client: TestClient):
    check_keys = [
        'id',
        'is_nsfw',
        'lang',
        'currency',
        'channel_id',
        'decrypted_token'
    ]
    count = random.randint(0, 50)
    for _ in range(count):
        create_random_webhook(db)

    response = client.get(v1_endpoint("/webhooks"))
    assert response.status_code == 200

    content = response.json()

    assert type(content) is list
    assert len(content) == count
    for webhook in content:
        for key in check_keys:
            assert key in webhook


def test_create_webhook(db: Session, client: TestClient, faker: Faker):
    channel_id = faker.numerify('%#################')
    data = {
        'id': "898012350",
        'token': "secrety",
        'is_nsfw': True,
        'lang': 'ja',
        'currency': 'JPY'
    }

    response = client.put(v1_endpoint(f"/webhooks/{channel_id}"), json=data)
    assert response.status_code == 201

    content = response.json()
    for key in data:
        if key == 'token':
            assert data.get(key) == content.get('decrypted_token')
        else:
            assert data.get(key) == content.get(key)


def test_get_webhook(db: Session, client: TestClient):
    webhook = create_random_webhook(db)
    check_keys = [
        'channel_id',
        'id',
        'decrypted_token',
        'is_existed',
        'lang',
        'currency',
        'created_at',
        'updated_at'
    ]

    response = client.get(v1_endpoint(f"/webhooks/{webhook.channel_id}"))
    assert response.status_code == 200
    content = response.json()
    for key in check_keys:
        assert key in content


def test_delete_webhook(db: Session, client: TestClient):
    webhook = create_random_webhook(db)
    channel_id = webhook.channel_id
    response = client.delete(
        v1_endpoint(f"/webhooks/{channel_id}")
    )
    assert response.status_code == 204

    response = client.delete(
        v1_endpoint(f"/webhooks/{channel_id}")
    )
    assert response.status_code == 404


def test_update_webhook_status(db: Session, client: TestClient):
    webhook = create_random_webhook(db)
    channel_id = webhook.channel_id
    exist_status = not webhook.is_existed
    response = client.patch(
        v1_endpoint(f"/webhooks/{channel_id}"),
        json={
            'is_existed': exist_status
        }
    )

    assert response.status_code == 200

    content = response.json()
    assert content.get('is_existed') is exist_status

    response = client.patch(
        v1_endpoint(f"/webhooks/123412341234"),
        json={
            'is_existed': exist_status
        }
    )
    assert response.status_code == 404
