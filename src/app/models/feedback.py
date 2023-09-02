from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class Feedback(SQLModel, table=True):
    msg_id: int | None = Field(default=None, foreign_key="message.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    mark_like: bool = False
    mark_dislike: bool = False
    content: str = ""
    update_time: datetime = Field(default_factory=datetime.now)

    # msg: "Message" = Relationship(back_populates="user_links")
    # user: "User" = Relationship(back_populates="msg_links")

class FeedbackRead(SQLModel):
    msg_id: int
    user_id: int
    mark_like: bool
    mark_dislike: bool
    content: str

class FeedbackUpdate(SQLModel):
    msg_id: int
    user_id: int | None = None
    mark_like: bool
    mark_dislike: bool
    content: str

__all__ = ["Feedback", "FeedbackRead", "FeedbackUpdate"]
