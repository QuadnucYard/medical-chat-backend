from typing import Any
from sqlmodel import SQLModel, select

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.chat import Chat, ChatCreate, ChatRead
from app.models.user import User


class CRUDChat(CRUDBase[Chat, ChatCreate, SQLModel]):
    async def get_by_userid(self, db: AsyncSession, *, user: User):
        return await db.run_sync(lambda _: user.chats)



chat = CRUDChat(Chat)
