from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class NoteBase(SQLModel):
    chat_id: int
    send_time: datetime
    content: str
    valid: bool = True


class Note(NoteBase, table=True):
    id: int = Field(default=None, primary_key=True)


class NoteRead(NoteBase):
    id: int


class NoteUpdate(NoteBase):
    ...


class NoteCreate(NoteUpdate):
    send_time: datetime = Field(default_factory=datetime.now)


__all__ = ["Note", "NoteUpdate", "NoteCreate", "NoteRead"]
