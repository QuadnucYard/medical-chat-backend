from sqlmodel.ext.asyncio.session import AsyncSession

from ai.pipeline import MedQAPipeline, PipelineResult
from aiapp.models import IntentCount, EntityCount
from aiapp import crud

pipeline = MedQAPipeline()


async def update_stats(db: AsyncSession, pr: PipelineResult):
    await crud.counter.inc(db, IntentCount, pr.detection.intent)
    for a in pr.answers:
        await crud.counter.inc(db, EntityCount, a.entity)


async def qa(db: AsyncSession, question: str | list[str]):
    res = await pipeline(question)
    for r in res if isinstance(res, list) else [res]:
        await update_stats(db, r)
    return res
