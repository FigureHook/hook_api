from app import crud
from app.models import Webhook
from app.schemas.webhook import WebhookCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_webhook(db: Session):
    lang = faker.random_choices(elements=Webhook.supporting_languages())[0]
    obj_data = WebhookCreate(
        channel_id=faker.numerify(
            text='%################'),
        id=faker.numerify(
            text='%################'),
        token=faker.lexify(text='???????????????????'),
        is_nsfw=faker.boolean(chance_of_getting_true=25),
        lang=lang)
    return crud.webhook.create(db=db, obj_in=obj_data)
