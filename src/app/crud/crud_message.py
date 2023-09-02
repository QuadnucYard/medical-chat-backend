from typing import Any
from sqlmodel import select

from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import get_password_hash, verify_password
from ..crud.base import CRUDBase
from ..models import Message, MessageRead, MessageCreate


class CRUDMessage(CRUDBase[Message, MessageCreate, CRUDBase]):
    async def create(self, db: AsyncSession, *, obj_in: MessageCreate) -> Message:
        db_obj = Message.from_orm(obj_in, {"chat_id": obj_in.chat_id})
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


message = CRUDMessage(Message)
