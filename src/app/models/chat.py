from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class ChatBase(SQLModel):
    user_id: int
    valid: bool = True
    share: int
    update_time: datetime
    title: str
    create_time: datetime


class Chat(ChatBase, table=True):
    id: int = Field(None, primary_key=True)


class ChatRead(ChatBase):
    id: int


class ChatUpdate(ChatBase):
    update_time: datetime = Field(default_factory=datetime.now)


class ChatCreate(ChatUpdate):
    create_time: datetime = Field(default_factory=datetime.now)


__all__ = ["Chat", "ChatRead", "ChatUpdate", "ChatCreate"]
