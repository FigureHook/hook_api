from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel


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
    last_seen_at: Union[datetime, None]

    class Config:
        orm_mode = True
