from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ApplicationBase(BaseModel):
    name: str


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    pass


class ApplicationInDB(ApplicationBase):
    id: UUID
    token: str
    created_at: datetime
    updated_at: datetime
    last_seen_at: datetime

    class Config:
        orm_mode = True
