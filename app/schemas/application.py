from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


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
    last_seen_at: Optional[datetime] = Field(nullable=True)

    class Config:
        orm_mode = True
