from pydantic import BaseModel
from uuid import UUID


class ApplicationBase(BaseModel):
    name: str


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    pass


class ApplicationInDB(ApplicationBase):
    id: UUID
    token: str
