
from typing import cast

from app.helpers.encrypt_helper import EncryptHelper
from sqlalchemy import Boolean, Column, String
from sqlalchemy.event import listens_for
from sqlalchemy.orm import validates
from sqlalchemy_mixins.timestamp import TimestampsMixin

from ..db.model_base import Model

__all__ = [
    "Webhook"
]


class Webhook(Model, TimestampsMixin):
    __tablename__ = "webhook"
    supporting_langs = ("zh-TW", "en", "ja")

    channel_id = cast(str, Column(String, primary_key=True))
    id = cast(str, Column(String, unique=True, nullable=False))
    token = cast(str, Column(String, nullable=False))
    is_existed = cast(bool, Column(Boolean))
    is_nsfw = cast(bool, Column(Boolean, default=False))
    lang = cast(str, Column(String(5), default="en"))

    @property
    def decrypted_token(self):
        return EncryptHelper.decrypt(self.token)

    @validates('lang')
    def validate_lang(self, key, lang):
        assert lang in self.supporting_langs, f"Language: {lang} is not supported now.\nCurrently supported language: {self.supporting_langs}"
        return lang

    @classmethod
    def supporting_languages(cls):
        return cls.supporting_langs


@listens_for(target=Webhook.token, identifier='set', retval=True)
def _webhook_attr_token_receive_set(target, token_value: str, old_token_value, initiator) -> str:
    return EncryptHelper.encrypt(token_value)
