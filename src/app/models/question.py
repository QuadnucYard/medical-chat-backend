from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class QuestionBase(SQLModel):
    chat_id: int
    user_id: int
    title: str
    content: str
    subject: enumerate
    end_time: datetime
    keywords: str


class Question(QuestionBase, table=True):
    id: int = Field(None, primary_key=True)


class QuestionRead(QuestionBase):
    id: int


__all__ = ["Question", "QuestionRead"]

