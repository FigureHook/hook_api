from app import crud
from app.api import deps
from app.models import Webhook
from app.schemas.webhook import (DecryptedWebhookInDB, EncryptedWebhookInDB,
                                 WebhookCreate, WebhookUpdate)
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
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


@router.post(
    "/",
    response_model=DecryptedWebhookInDB,
    status_code=status.HTTP_201_CREATED)
def create_webhook(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    webhook_item: WebhookCreate
):
    webhook = crud.webhook.get(db=db, id=webhook_item.channel_id)
    if webhook:
        return RedirectResponse(
            url=request.url_for('get_webhook', channel_id=webhook.channel_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    webhook = crud.webhook.create(db=db, obj_in=webhook_item)
    return DecryptedWebhookInDB.from_orm(webhook)


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
    db: Session = Depends(deps.get_db),
    data_in: WebhookUpdate,
    webhook: Webhook = Depends(check_webhook_exist)
):
    crud.webhook.update(db=db, db_obj=webhook, obj_in=data_in)
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
    response_model=EncryptedWebhookInDB)
def patch_webhook(
    *,
    db: Session = Depends(deps.get_db),
    webhook: Webhook = Depends(check_webhook_exist),
    patch_data: WebhookUpdate
):
    crud.webhook.update(db=db, db_obj=webhook, obj_in=patch_data)
    return EncryptedWebhookInDB.from_orm(webhook)

