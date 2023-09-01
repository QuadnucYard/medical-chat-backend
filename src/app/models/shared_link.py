from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid1
from sqlalchemy import TIMESTAMP, Column

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .chat import Chat
from .shared_user import SharedUser


class SharedLinkBase(SQLModel):
    link: str
    create_time: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    expire_time: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    max_uses: int
    readonly: bool
    valid: bool = True


class SharedLink(SharedLinkBase, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int | None = Field(default=None, foreign_key="chat.id")
    create_time: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True)),
    )
    link: str | None = Field(default_factory=lambda: str(uuid1()).replace("-", ""))

    chat: "Chat" = Relationship(back_populates="links")

    user_links: list["SharedUser"] = Relationship(back_populates="link")


class SharedLinkRead(SharedLinkBase):
    id: int


class SharedLinkCreate(SQLModel):
    chat_id: int
    expire_time: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    max_uses: int
    readonly: bool
    valid: bool = True


__all__ = ["SharedLink", "SharedLinkCreate", "SharedLinkRead"]
