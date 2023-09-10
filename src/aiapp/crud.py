from typing import Type

from sqlmodel.ext.asyncio.session import AsyncSession

from aiapp.models import BaseCount


class CRUDCounter:
    async def inc(self, db: AsyncSession, model: Type[BaseCount], key: str):
        obj = await db.get(model, key) or model(key=key)
        obj.value += 1
        db.add(obj)
        await db.commit()

counter = CRUDCounter()