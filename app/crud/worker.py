from app.models import Paintwork, Sculptor
from app.schemas.worker import WorkerCreate, WorkerUpdate
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDSculptor(CRUDBase[Sculptor, WorkerCreate, WorkerUpdate]):
    pass


class CRUDPaintwork(CRUDBase[Paintwork, WorkerCreate, WorkerUpdate]):
    pass


paintwork = CRUDPaintwork(Paintwork)
sculptor = CRUDSculptor(Sculptor)
