from datetime import datetime
from typing import Optional

from app.constants import WebhookCurrency, WebhookLang
from pydantic import BaseModel, Field


class WebhookBase(BaseModel):
    id: str
    token: str
    channel_id: str
    guild_id: str
    is_nsfw: Optional[bool] = Field(default=True)
    lang: Optional[WebhookLang] = Field(default=WebhookLang.EN)
    currency: Optional[WebhookCurrency] = Field(default=WebhookCurrency.JPY)


class WebhookCreate(WebhookBase):
    pass


class WebhookDBCreate(WebhookCreate):
    channel_id: str


class WebhookUpdate(BaseModel):
    is_existed: Optional[bool] = Field(nullable=True)


class WebhookInDBBase(WebhookBase):
    is_existed: Optional[bool] = Field(nullable=True)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DecryptedWebhookInDB(WebhookInDBBase):
    decrypted_token: str
