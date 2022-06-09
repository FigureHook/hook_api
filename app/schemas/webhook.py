from datetime import datetime
from typing import Optional

from app.constants import WebhookCurrency, WebhookLang
from pydantic import BaseModel, Field
from this import d


class WebhookBase(BaseModel):
    id: str
    is_nsfw: bool
    lang: Optional[WebhookLang] = Field(default=WebhookLang.EN)
    currency: Optional[WebhookCurrency] = Field(default=WebhookCurrency.JPY)


class WebhookCreate(WebhookBase):
    channel_id: str
    token: str


class WebhookUpdate(WebhookBase):
    is_existed: Optional[bool]
    token: str


class WebhookInDBBase(WebhookBase):
    channel_id: str
    is_existed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EncryptedWebhookInDB(WebhookInDBBase):
    token: str


class DecryptedWebhookInDB(WebhookInDBBase):
    decrypted_token: str
