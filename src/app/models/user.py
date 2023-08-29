from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class UserBase(SQLModel):
    uname: str
    email: str


class User(UserBase, table=True):
    id: int = Field(None, primary_key=True)
    password: str


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...
