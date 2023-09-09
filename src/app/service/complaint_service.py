from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.utils.statutils import counter_helper


async def get_temporal_stats(db: AsyncSession):
    return await counter_helper(
        db,
        (crud.complaint.count_by_create_date, "creation"),
        (crud.complaint.count_by_resolve_date, "resolution"),
    )
