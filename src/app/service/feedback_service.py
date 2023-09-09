from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.utils.statutils import counter_helper


async def get_temporal_stats(db: AsyncSession):
    return await counter_helper(
        db,
        (crud.feedback.count_by_update_date, "total"),
        (crud.feedback.count_like_by_update_date, "like"),
        (crud.feedback.count_dislike_by_update_date, "dislike"),
        (crud.feedback.count_comment_by_update_date, "comments"),
    )
