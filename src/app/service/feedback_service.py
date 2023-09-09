import pandas as pd
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud


async def get_stats(db: AsyncSession):
    a = await crud.feedback.count_by_update_date(db)
    b = await crud.feedback.count_like_by_update_date(db)
    c = await crud.feedback.count_dislike_by_update_date(db)
    d = await crud.feedback.count_comment_by_update_date(db)
    res = pd.concat(
        [
            pd.DataFrame(a).set_index("date").rename(columns={"count": "total"}),
            pd.DataFrame(b).set_index("date").rename(columns={"count": "like"}),
            pd.DataFrame(c).set_index("date").rename(columns={"count": "dislike"}),
            pd.DataFrame(d).set_index("date").rename(columns={"count": "comments"}),
        ],
        axis=1,
        join="inner",
    ).sort_index().fillna(0)
    res.insert(0, "date", res.index)
    return res.to_dict("records")
