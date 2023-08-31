from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class Shared_linkBase(SQLModel):
    link: int
    expire_time: datetime
    uses: int
    readonly: bool
    valid: bool
    create_time: datetime


class Shared_link(Shared_linkBase, table=True):
    chat_id: int = Field(None, foreign_key=True)


class Shared_linkRead(Shared_linkBase):
    id: int


class Shared_linkUpdate(Shared_linkBase):
    ...


class Shared_linkCreate(Shared_linkUpdate):
    send_time: datetime = Field(default_factory=datetime.now)


__all__ = ["Shared_link", "Shared_linkUpdate", "Shared_linkCreate", "Shared_linkRead"]
