from typing import Optional

from app.models import Webhook
from pydantic import BaseModel, constr, validator


def _validate_lang(lang: str) -> str:
    suuporing_langs = Webhook.supporting_languages()
    if lang not in suuporing_langs:
        raise ValueError(
            f"Language: {lang} is not supported now.\nCurrently supported language: {suuporing_langs}"
        )
    return lang


class WebhookBase(BaseModel):
    id: str
    token: str
    is_nsfw: bool
    lang: str  # type: ignore

    @validator('lang')
    def validate_lang(cls, lang_v):
        return _validate_lang(lang_v)


class WebhookCreate(WebhookBase):
    channel_id: str


class WebhookUpdate(WebhookBase):
    is_existed: Optional[bool]


class WebhookInDB(WebhookBase):
    channel_id: str
    token: str
    is_nsfw: bool
    lang: str
    is_existed: bool
