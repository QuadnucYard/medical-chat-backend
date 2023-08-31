from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class AdminBase(SQLModel):
    username: str
    valid: bool = True
    login_time: datetime | None = None


class Admin(AdminBase, table=True):
    id: int = Field(None, primary_key=True)


class AdminRead(AdminBase):
    id: int


class AdminUpdate(AdminBase):
    ...


class AdminCreate(AdminUpdate):
    ...


__all__ = ["Admin", "AdminUpdate", "AdminCreate", "AdminRead"]
