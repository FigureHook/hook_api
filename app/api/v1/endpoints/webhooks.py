from app import crud
from app.api import deps
from app.models import Webhook
from app.schemas.webhook import (DecryptedWebhookInDB, WebhookCreate,
                                 WebhookDBCreate,
                                 WebhookUpdate)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

router = APIRouter()


def check_webhook_exist(channel_id: str, db: Session = Depends(deps.get_db)) -> Webhook:
    webhook = crud.webhook.get(db=db, id=channel_id)
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified webhook(channel_id:{channel_id}) didn't exist."
        )
    return webhook


@router.get(
    "/",
    response_model=list[DecryptedWebhookInDB],
    response_model_exclude_none=True)
def get_webhooks(
    *,
    db: Session = Depends(deps.get_db)
):
    webhooks = db.query(Webhook).all()
    return [
        DecryptedWebhookInDB.from_orm(webhook)
        for webhook in webhooks
    ]


@router.get(
    "/{channel_id}",
    response_model=DecryptedWebhookInDB)
def get_webhook(
    *,
    webhook: Webhook = Depends(check_webhook_exist)
):
    return DecryptedWebhookInDB.from_orm(webhook)


@router.put(
    "/{channel_id}",
    response_model=DecryptedWebhookInDB)
def update_webhook(
    *,
    response: Response,
    db: Session = Depends(deps.get_db),
    webhook_in: WebhookCreate,
    channel_id: str
):
    webhook = crud.webhook.get(db=db, id=channel_id)

    if webhook:
        crud.webhook.update(db=db, db_obj=webhook, obj_in=webhook_in)
        response.status_code = status.HTTP_200_OK
    else:
        webhook_item = WebhookDBCreate(
            channel_id=channel_id,
            id=webhook_in.id,
            token=webhook_in.token,
            is_nsfw=webhook_in.is_nsfw,
            lang=webhook_in.lang,
            currency=webhook_in.currency
        )
        webhook_in = WebhookDBCreate.parse_obj(webhook_item)
        webhook = crud.webhook.create(db=db, obj_in=webhook_in)
        response.status_code = status.HTTP_201_CREATED

    return DecryptedWebhookInDB.from_orm(webhook)


@router.delete(
    "/{channel_id}",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_webhook(
    *,
    db: Session = Depends(deps.get_db),
    webhook: Webhook = Depends(check_webhook_exist)
):
    crud.webhook.remove(db=db, id=webhook.channel_id)


@router.patch(
    "/{channel_id}",
    response_model=DecryptedWebhookInDB)
def patch_webhook(
    *,
    db: Session = Depends(deps.get_db),
    webhook: Webhook = Depends(check_webhook_exist),
    patch_data: WebhookUpdate
):
    crud.webhook.update(db=db, db_obj=webhook, obj_in=patch_data)
    return DecryptedWebhookInDB.from_orm(webhook)
