import logging

from app import crud
from app.api import deps
from app.models import Webhook
from app.schemas.webhook import (
    DecryptedWebhookInDB,
    WebhookCreate,
    WebhookDBCreate,
    WebhookUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(__name__)


def check_webhook_exist(webhook_id: str, db: Session = Depends(deps.get_db)) -> Webhook:
    webhook = crud.webhook.get(db=db, id=webhook_id)
    if not webhook:
        logger.info(f"Specified webhook didn't exist. (webhook_id={webhook_id})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified webhook(webhook_id:{webhook_id}) didn't exist.",
        )
    return webhook


@router.get(
    "/", response_model=list[DecryptedWebhookInDB], response_model_exclude_none=True
)
async def get_webhooks(*, db: Session = Depends(deps.get_db)):
    webhooks = db.query(Webhook).all()
    logger.info(f"Fetched the webhooks. (count={len(webhooks)})")
    return [DecryptedWebhookInDB.from_orm(webhook) for webhook in webhooks]


@router.get("/{webhook_id}", response_model=DecryptedWebhookInDB)
async def get_webhook(
    *, webhook: Webhook = Depends(check_webhook_exist), webhook_id: str
):
    logger.info(f"Fetched the webhook. (webhook_id={webhook_id})")
    return DecryptedWebhookInDB.from_orm(webhook)


@router.put("/{webhook_id}", response_model=DecryptedWebhookInDB)
async def update_webhook(
    *,
    response: Response,
    db: Session = Depends(deps.get_db),
    webhook_in: WebhookCreate,
    webhook_id: str,
):
    webhook = crud.webhook.get(db=db, id=webhook_id)

    if webhook:
        crud.webhook.update(db=db, db_obj=webhook, obj_in=webhook_in)
        response.status_code = status.HTTP_200_OK
        logger.info(f"Updated the webhook. (webhook_id={webhook_id})")
    else:
        webhook = crud.webhook.create(db=db, obj_in=webhook_in)
        response.status_code = status.HTTP_201_CREATED
        logger.info(f"Created the webhook. (webhook_id={webhook_id})")

    return DecryptedWebhookInDB.from_orm(webhook)


@router.delete("/{webhook_id}")
async def delete_webhook(
    *,
    db: Session = Depends(deps.get_db),
    webhook: Webhook = Depends(check_webhook_exist),
    webhook_id: str,
):
    crud.webhook.remove(db=db, id=webhook.id)
    logger.info(f"Removed the webhook. (webhook_id={webhook_id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{webhook_id}", response_model=DecryptedWebhookInDB)
async def patch_webhook(
    *,
    db: Session = Depends(deps.get_db),
    webhook: Webhook = Depends(check_webhook_exist),
    patch_data: WebhookUpdate,
    webhook_id: str,
):
    crud.webhook.update(db=db, db_obj=webhook, obj_in=patch_data)
    logger.info(f"Updated the webhook. (webhook_id={webhook_id})")
    return DecryptedWebhookInDB.from_orm(webhook)
