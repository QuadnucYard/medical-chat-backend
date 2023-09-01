from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
from sqlalchemy.orm import relationship

# relationship(,)


class ComplaintBase(SQLModel):
    content: str
    create_time: datetime
    resolve_time: datetime | None  # None as unresolved


class Complaint(ComplaintBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    admin_id: int | None = Field(default=None, foreign_key="user.id")

    user: "User" = Relationship(
        back_populates="posted_complaints",
        sa_relationship_kwargs=dict(primaryjoin="Complaint.user_id==User.id", lazy="joined"),
    )
    admin: "User" = Relationship(
        back_populates="resolved_complaints",
        sa_relationship_kwargs=dict(primaryjoin="Complaint.admin_id==User.id", lazy="joined"),
    )


class ComplaintRead(ComplaintBase):
    id: int
    user_id: int
    admin_id: int


class ComplaintCreate(ComplaintBase):
    create_time: datetime = Field(default_factory=datetime.now)


__all__ = ["Complaint", "ComplaintCreate", "ComplaintRead"]
