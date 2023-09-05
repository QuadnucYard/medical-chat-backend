from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.role_perm import PermRead

if TYPE_CHECKING:
    from . import Chat, Complaint, PermRead, Role, RoleRead, SharedUser


class UserBase(SQLModel):
    username: str
    email: str = Field(default="", index=True)
    phone: str = Field(default="", index=True)
    name: str = ""
    avatar_url: str = ""
    create_time: datetime = Field(default_factory=datetime.now)
    login_time: datetime | None = None
    update_time: datetime = Field(default_factory=datetime.now)
    is_superuser: bool = False
    role_id: int | None = Field(default=None, foreign_key="role.id")
    valid: bool = True


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str

    role: "Role" = Relationship(back_populates="users")
    chats: list["Chat"] = Relationship(back_populates="user")
    links: list["SharedUser"] = Relationship(back_populates="user")
    posted_complaints: list["Complaint"] = Relationship(
        back_populates="user", sa_relationship_kwargs=dict(foreign_keys="Complaint.user_id")
    )
    resolved_complaints: list["Complaint"] = Relationship(
        back_populates="admin", sa_relationship_kwargs=dict(foreign_keys="Complaint.admin_id")
    )


class UserRead(UserBase):
    id: int
    create_time: datetime
    update_time: datetime


class UserReadPartial(SQLModel):
    id: int
    username: str
    avatar_url: str


class UserReadWithRole(UserRead):
    role: "RoleRead"


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


__all__ = ["User", "UserRead", "UserReadWithRole", "UserReadPartial", "UserUpdate", "UserCreate", "UserRegister"]

from .role_perm import RoleRead

UserRead.update_forward_refs()
