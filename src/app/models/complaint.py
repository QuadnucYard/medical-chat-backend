from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class ComplaintBase(SQLModel):
    user_id: int
    admin_id: int
    content: str
    create_time: datetime
    resolve_time: datetime
    content: str
    resolved: bool


class Complaint(ComplaintBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ComplaintRead(ComplaintBase):
    id: int


class ComplaintUpdate(ComplaintBase):
    ...


class ComplaintCreate(ComplaintUpdate):
    create_time: datetime = Field(default_factory=datetime.now)


__all__ = ["Complaint", "ComplaintCreate", "ComplaintUpdate", "ComplaintRead"]
