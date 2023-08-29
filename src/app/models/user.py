from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class UserBase(SQLModel):
    username: str
    email: str = Field(default="", index=True)
    phone: str = Field(default="", index=True)
    name: str = ""
    avatar_url: str = ""
    create_time: datetime
    login_time: datetime | None = None
    update_time: datetime
    is_superuser: bool = False
    valid: bool = True


class User(UserBase, table=True):
    id: int = Field(None, primary_key=True)
    hashed_password: str


class UserRead(UserBase):
    id: int


class UserUpdate(UserBase):
    password: str
    update_time: datetime = Field(default_factory=datetime.now)


class UserCreate(UserUpdate):
    create_time: datetime = Field(default_factory=datetime.now)


class UserRegister(SQLModel):
    username: str
    password: str
    email: str = Field(default="", index=True)
    phone: str = Field(default="", index=True)
    name: str = ""


__all__ = ["User", "UserRead", "UserUpdate", "UserCreate", "UserRegister"]
