from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class RolePermLink(SQLModel, table=True):
    role_id: int | None = Field(default=None, foreign_key="role.id", primary_key=True)
    perm_id: int | None = Field(default=None, foreign_key="perm.id", primary_key=True)


class RoleBase(SQLModel):
    name: str
    enabled: bool = True


class Role(RoleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    perms: list["Perm"] = Relationship(back_populates="roles", link_model=RolePermLink)
    users: list["User"] = Relationship(back_populates="role")

class RoleRead(RoleBase):
    id: int
    perms: list["Perm"]


class PermBase(SQLModel):
    name: str
    desc: str
    route: str
    enabled: bool = True


class Perm(PermBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    roles: list["Role"] = Relationship(back_populates="perms", link_model=RolePermLink)


class PermRead(PermBase):
    id: int


__all__ = ["Perm", "PermRead", "Role", "RoleRead", "RolePermLink"]
