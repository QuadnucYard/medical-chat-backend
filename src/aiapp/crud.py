from typing import Type

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from aiapp.models import BaseCount


class CRUDCounter:
    async def gets(self, db: AsyncSession, model: Type[BaseCount]) -> list[BaseCount]:
        stmt = select(model)
        return (await db.exec(stmt)).all()  # type: ignore

    async def inc(self, db: AsyncSession, model: Type[BaseCount], key: str):
        obj = await db.get(model, key) or model(key=key)
        obj.value += 1
        db.add(obj)
        await db.commit()


counter = CRUDCounter()
