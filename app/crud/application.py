from app.models import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

from .base import CRUDBase


class CRUDApplication(CRUDBase[Application, ApplicationCreate, ApplicationUpdate]):
    pass


application = CRUDApplication(Application)
