from app import crud
from app.constants import WebhookCurrency, WebhookLang
from app.schemas.webhook import WebhookCreate, WebhookUpdate, WebhookDBCreate
from app.tests.utils.faker import faker
from app.tests.utils.webhook import create_random_webhook
from sqlalchemy.orm import Session


def test_create_webhook(db: Session):
    obj_in = WebhookDBCreate(
        channel_id=faker.numerify(
            text='%################'),
        id=faker.numerify(
            text='%################'),
        token=faker.lexify(text='???????????????????'),
        is_nsfw=faker.boolean(chance_of_getting_true=25),
        lang=faker.random_choices(elements=WebhookLang)[0],
        currency=faker.random_choices(elements=WebhookCurrency)[0]
    )

    db_obj = crud.webhook.create(db=db, obj_in=obj_in)
    assert db_obj.channel_id == obj_in.channel_id
    assert db_obj.id == obj_in.id
    assert db_obj.lang == obj_in.lang
    assert db_obj.token != obj_in.token
    assert db_obj.decrypted_token == obj_in.token
    assert db_obj.is_nsfw == obj_in.is_nsfw


def test_get_webhook(db: Session):
    db_obj = create_random_webhook(db=db)
    fetched_db_obj = crud.webhook.get(db=db, id=db_obj.channel_id)

    assert fetched_db_obj == db_obj


def test_update_webhook(db: Session):
    db_obj = create_random_webhook(db=db)

    obj_in = WebhookCreate(
        id=faker.numerify(text='%################'),
        token=faker.lexify(text='???????????????????'),
        is_nsfw=faker.boolean(chance_of_getting_true=25),
        lang=faker.random_choices(elements=WebhookLang)[0],
        currency=faker.random_choices(elements=WebhookCurrency)[0],
    )

    udpated_db_obj = crud.webhook.update(db=db, db_obj=db_obj, obj_in=obj_in)
    assert obj_in.id == udpated_db_obj.id
    assert obj_in.token == udpated_db_obj.decrypted_token
    assert obj_in.is_nsfw == udpated_db_obj.is_nsfw
    assert obj_in.lang == udpated_db_obj.lang


def test_remove_webhook(db: Session):
    db_obj = create_random_webhook(db=db)

    deleted_db_obj = crud.webhook.remove(db=db, id=db_obj.channel_id)
    fetched_db_obj = crud.webhook.get(db=db, id=db_obj.channel_id)

    assert not fetched_db_obj
    if deleted_db_obj:
        assert deleted_db_obj == db_obj
