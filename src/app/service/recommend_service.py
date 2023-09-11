from datetime import datetime
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.models import User, Recommendation, RecommendationCreate, PageParams


async def get_active_recommends(db: AsyncSession):
    return await crud.recommend.get_active_ones(db)


async def get_all_recommends(db: AsyncSession, page: PageParams, active: bool | None):
    if active is None:
        return await crud.recommend.get_page(db, page=page)
    elif active:
        return await crud.recommend.get_page_if(db, Recommendation.remove_time == None, page=page)
    else:
        return await crud.recommend.get_page_if(db, Recommendation.remove_time != None, page=page)


async def add_recommend(db: AsyncSession, obj_in: RecommendationCreate, user: User):
    return await crud.recommend.add(
        db, Recommendation(title=obj_in.title, content=obj_in.content, creator=user)
    )


async def remove_recommend(db, rec_id: int, user: User):
    rec = await crud.recommend.get(db, rec_id)
    if not rec:
        return None
    rec.remove_time = datetime.now()
    rec.remover = user
    return await crud.recommend.add(db, rec)

async def recover_recommend(db, rec_id: int, user: User):
    rec = await crud.recommend.get(db, rec_id)
    if not rec:
        return None
    rec.remove_time = None
    rec.remover = None
    return await crud.recommend.add(db, rec)
