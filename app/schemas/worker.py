from pydantic import BaseModel


class WorkerBase(BaseModel):
    name: str


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(WorkerBase):
    pass


class WorkerInDB(WorkerBase):
    id: int

    class Config:
        orm_mode = True
