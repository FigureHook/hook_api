import secrets
from datetime import datetime

from app.db.model_base import UUIDPkModel
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func

__all__ = ["Application"]


def _generate_token():
    return secrets.token_urlsafe(64)


class Application(UUIDPkModel):
    __tablename__ = "application"

    name: Mapped[str] = Column(String, nullable=False)  # type: ignore
    token: Mapped[str] = Column(String, default=_generate_token)  # type: ignore
    last_seen_at: Mapped[datetime] = Column(DateTime)  # type: ignore

    def refresh_token(self):
        self.token = _generate_token()
        return self

    def was_seen(self):
        self.last_seen_at = func.now()
        return self
