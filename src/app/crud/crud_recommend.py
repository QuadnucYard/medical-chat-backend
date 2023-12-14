from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.recommendation import Recommendation, RecommendationCreate


class CRUDRecommend(CRUDBase[Recommendation, RecommendationCreate, SQLModel]):
    async def get_active_ones(self, db: AsyncSession):
        stmt = select(Recommendation).where(Recommendation.remove_time == None)
        return (await db.scalars(stmt)).all()


recommend = CRUDRecommend(Recommendation)
