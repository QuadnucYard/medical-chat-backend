from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .user import User
    from ..models.shared_link import SharedLink
    from .message import Message


class ChatBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    title: str
    update_time: datetime
    create_time: datetime
    delete_time: datetime | None = None  # None as valid


class Chat(ChatBase, table=True):
    id: int = Field(default=None, primary_key=True)
    create_time: datetime = Field(default_factory=datetime.now)
    update_time: datetime = Field(default_factory=datetime.now)
    user: "User" = Relationship(back_populates="chats")
    messages: list["Message"] = Relationship(back_populates="chat")
    links: list["SharedLink"] = Relationship(back_populates="chat")


class ChatRead(ChatBase):
    id: int
    user_id: int
    user: "User"


class ChatReadWithMessages(ChatRead):
    messages: list["Message"] = Relationship(back_populates="chat")


class ChatCreate(ChatBase):
    user_id: int
    title: str


__all__ = ["Chat", "ChatRead", "ChatReadWithMessages", "ChatCreate"]
