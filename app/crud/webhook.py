from app.models import Webhook
from app.schemas.webhook import WebhookCreate, WebhookUpdate

from .base import CRUDBase


class CRUDWebhook(CRUDBase[Webhook, WebhookCreate, WebhookUpdate]):
    pass


webhook = CRUDWebhook(Webhook)
