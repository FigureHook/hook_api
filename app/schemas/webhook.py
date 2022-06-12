from datetime import datetime
from optparse import Option
from typing import Optional

from app.constants import WebhookCurrency, WebhookLang
from pydantic import BaseModel, Field


class WebhookBase(BaseModel):
    id: Optional[str]
    is_nsfw: Optional[bool]
    lang: Optional[WebhookLang]
    currency: Optional[WebhookCurrency]


class WebhookCreate(WebhookBase):
    channel_id: str
    id: str
    token: str
    is_nsfw: Optional[bool] = Field(default=True)
    lang: Optional[WebhookLang] = Field(default=WebhookLang.EN)
    currency: Optional[WebhookCurrency] = Field(default=WebhookCurrency.JPY)


class WebhookUpdate(WebhookBase):
    is_existed: Optional[bool]
    token: Optional[str]


class WebhookInDBBase(WebhookBase):
    channel_id: str
    is_existed: Optional[bool]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EncryptedWebhookInDB(WebhookInDBBase):
    token: str


class DecryptedWebhookInDB(WebhookInDBBase):
    decrypted_token: str
