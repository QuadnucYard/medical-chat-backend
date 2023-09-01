from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .chat import Chat
from .shared_user import SharedUser


class SharedLinkBase(SQLModel):
    link: str
    create_time: datetime
    expire_time: datetime
    max_uses: int
    readonly: bool
    valid: bool = True


class SharedLink(SharedLinkBase, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(default=None, foreign_key="chat.id")

    chat: "Chat" = Relationship(back_populates="links")

    user_links: list["SharedUser"] = Relationship(back_populates="link")


class SharedLinkRead(SharedLinkBase):
    id: int


class SharedLinkCreate(SQLModel):
    create_time: datetime = Field(default_factory=datetime.now)


__all__ = ["SharedLink", "SharedLinkCreate", "SharedLinkRead"]
