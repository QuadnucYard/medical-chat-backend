from typing import Any
from sqlmodel import SQLModel, select

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import Message, MessageRead, MessageCreate
from app.models.message import MessageType


class CRUDMessage(CRUDBase[Message, MessageCreate, SQLModel]):
    async def count_by_date(self, db):
        return await super().count_by_date(db, Message.send_time)

    async def count_q_by_date(self, db):
        return await super().count_if_by_date(
            db, Message.send_time, Message.type == MessageType.Question
        )

    async def count_a_by_date(self, db):
        return await super().count_if_by_date(
            db, Message.send_time, Message.type == MessageType.Answer
        )

    async def count_n_by_date(self, db):
        return await super().count_if_by_date(
            db, Message.send_time, Message.type == MessageType.Note
        )


message = CRUDMessage(Message)
