from typing import Type

from sqlmodel.ext.asyncio.session import AsyncSession

from aiapp import crud
from aiapp.models import BaseCount, EntityCount, IntentCount, WordCount


async def make_dict(db: AsyncSession, model: Type[BaseCount], trans: dict[str, str] | None = None):
    if trans is None:
        trans = {}
    res = await crud.counter.gets(db, model)
    return {trans.get(c.key, c.key): c.value for c in res}


intent_trans = {"disease_prevent": "预防"}


async def get_counters(db: AsyncSession):
    return {
        "word": await make_dict(db, WordCount),
        "intent": await make_dict(db, IntentCount, intent_trans),
        "entity": await make_dict(db, EntityCount),
    }
