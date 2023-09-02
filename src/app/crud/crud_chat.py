from typing import Any
from sqlmodel import select

from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.security import get_password_hash, verify_password
from ..crud.base import CRUDBase
from ..models.chat import Chat, ChatCreate, ChatRead


class CRUDChat(CRUDBase[Chat, ChatCreate, CRUDBase]):
    """def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()"""

    async def get_by_chat_id(self, db: AsyncSession, *, chat_id):
        query = select(Chat).where(Chat.id == chat_id)
        return (await db.exec(query)).first()

    async def get_by_userid(self, db: AsyncSession, *, userid):
        query = select(Chat).where(Chat.user_id == userid)
        return (await db.exec(query)).first()

    async def create(self, db: AsyncSession, *, obj_in: ChatCreate) -> Chat:
        db_obj = Chat.from_orm(obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj




chat = CRUDChat(Chat)
