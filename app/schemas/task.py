from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    name: str
    executed_at: datetime


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: int
