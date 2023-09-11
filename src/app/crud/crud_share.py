from datetime import datetime, timezone
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import SharedLink, SharedLinkCreate, SharedUser, User


class CRUDShare(CRUDBase[SharedLink, SharedLinkCreate, BaseModel]):
    async def is_user_shared(self, db: AsyncSession, user_id: int, link_id: str):
        stmt = select(SharedUser).where(
            SharedUser.user_id == user_id, SharedUser.link_id == link_id
        )
        return (await db.exec(stmt)).first() is not None  # type: ignore

    async def get_shared_times(self, db: AsyncSession, link_id: str):
        link = await self.get(db, link_id)
        return link.use_times if link else 0

    async def consume_share(self, db: AsyncSession, user: User, link: SharedLink):
        su = SharedUser(user=user, link=link)
        db.add(su)
        await db.commit()
        await db.refresh(su)
        return su

    async def add_share(self, db: AsyncSession, link: SharedLink, user: User):
        link.use_times += 1
        db.add(link)
        await db.commit()
        await db.refresh(link)
        await self.consume_share(db, user=user, link=link)
        return link
    
    def is_expired(self, link: SharedLink):
        return link.expire_time < datetime.now(timezone.utc)


share = CRUDShare(SharedLink)
