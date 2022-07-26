from typing import Optional

from app.models import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDApplication(CRUDBase[Application, ApplicationCreate, ApplicationUpdate]):
    def get_by_token(self, *, db: Session, token: str) -> Optional[Application]:
        return db.query(self.model).filter(Application.token == token).first()


application = CRUDApplication(Application)
