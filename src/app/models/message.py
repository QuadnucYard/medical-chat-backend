from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .chat import Chat


class MessageType(Enum):
    Question = 0
    Answer = 1


class MessageBase(SQLModel):
    chat_id: int | None = Field(default=None, foreign_key="chat.id")
    type: MessageType
    content: str


class Message(MessageBase, table=True):
    id: int = Field(default=None, primary_key=True)
    send_time: datetime = Field(default_factory=datetime.now)

    chat: "Chat" = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    id: int
    send_time: datetime
    chat_id: int


class MessageCreate(MessageBase):
    chat_id: int


__all__ = ["MessageType", "Message", "MessageRead", "MessageCreate"]
