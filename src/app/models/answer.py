from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    ...


class AnswerBase(SQLModel):
    qid: int
    send_time: datetime

    mark_like: bool
    mark_dislike: bool


class Answer(AnswerBase, table=True):
    id: int = Field(None, primary_key=True)


class AnswerRead(AnswerBase):
    id: int


class AnswerUpdate(AnswerBase):
    ...


class AnswerCreate(AnswerUpdate):
    send_time: datetime = Field(default_factory=datetime.now)


__all__ = ["Answer", "AnswerRead", "AnswerCreate", "AnswerUpdate"]
