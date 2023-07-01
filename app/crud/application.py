from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

from .base import CRUDBase


class CRUDApplication(CRUDBase[Application, ApplicationCreate, ApplicationUpdate]):
    def get_by_token(self, *, db: Session, token: str) -> Optional[Application]:
        stmt = select(self.model).filter(self.model.token == token)
        result = db.execute(stmt)
        return result.scalar(result)


application = CRUDApplication(Application)
