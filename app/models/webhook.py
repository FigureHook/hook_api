from app.constants import WebhookCurrency, WebhookLang
from app.helpers.encrypt_helper import EncryptHelper
from sqlalchemy import Boolean, Column, String
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped
from sqlalchemy_mixins.timestamp import TimestampsMixin

from ..db.model_base import Model

__all__ = ["Webhook"]


class Webhook(Model, TimestampsMixin):
    __tablename__ = "webhook"

    channel_id: Mapped[str] = Column(String, primary_key=True)  # type: ignore
    id: Mapped[str] = Column(String, unique=True, nullable=False)  # type: ignore
    token: Mapped[str] = Column(String, nullable=False)  # type: ignore
    is_existed: Mapped[str] = Column(Boolean)  # type: ignore
    is_nsfw: Mapped[str] = Column(Boolean, default=False)  # type: ignore
    lang: Mapped[str] = Column(String(5), default=WebhookLang.EN)  # type: ignore
    currency: Mapped[str] = Column(
        String(3), default=WebhookCurrency.JPY, comment="ISO 4217"
    )  # type: ignore

    @property
    def decrypted_token(self):
        return EncryptHelper.decrypt(self.token)


@listens_for(target=Webhook.token, identifier="set", retval=True)
def _webhook_attr_token_receive_set(
    target, token_value: str, old_token_value, initiator
) -> str:
    return EncryptHelper.encrypt(token_value)
