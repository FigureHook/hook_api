from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate

from .base import CRUDBase


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    pass


task = CRUDTask(Task)
