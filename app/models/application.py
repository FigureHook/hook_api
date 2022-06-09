import secrets

from app.db.model_base import UUIDPkModel
from sqlalchemy import Column, String, DateTime

__all__ = ['Application']


def _generate_token():
    return secrets.token_urlsafe(64)


class Application(UUIDPkModel):
    __tablename__ = "application"

    name = Column(String, nullable=False)
    token = Column(String, default=_generate_token)
    last_seen_at = Column(DateTime)

    def refresh_token(self):
        self.token = _generate_token()
        return self
