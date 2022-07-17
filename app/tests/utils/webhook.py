from app import crud
from app.constants import WebhookCurrency, WebhookLang
from app.schemas.webhook import WebhookDBCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_webhook(db: Session):
    lang = faker.random_choices(elements=WebhookLang)[0]
    currency = faker.random_choices(elements=WebhookCurrency)[0]
    obj_data = WebhookDBCreate(
        channel_id=faker.numerify(
            text='%################'),
        id=faker.numerify(
            text='%################'),
        token=faker.lexify(text='???????????????????'),
        is_nsfw=faker.boolean(chance_of_getting_true=25),
        lang=lang,
        currency=currency
    )
    return crud.webhook.create(db=db, obj_in=obj_data)
