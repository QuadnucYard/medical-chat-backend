from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.db.utils import from_orm_async
from app.routers import deps

router = APIRouter()


@router.get("/", response_model=list[models.FeedbackReadWithMsgUser])
async def get_feedbacks(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: deps.QueryParams = Depends(),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all feedbacks."""
    feedbacks = await crud.feedback.gets(db, offset=q.offset, limit=q.limit)
    return await from_orm_async(db, models.FeedbackReadWithMsgUser, feedbacks)


@router.post("/", response_model=models.FeedbackRead)
async def update_feedback(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.FeedbackUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Update feedback of the user. Create feedback if necessary."""
    if data.mark_dislike:
        data.mark_like = False  # Exclusive
    fb = await crud.feedback.get(db, (data.msg_id, current_user.id))
    if fb:
        fb.update_time = datetime.now()
        return await crud.feedback.update(db, db_obj=fb, obj_in=data)
    else:
        msg = await crud.message.get(db, data.msg_id)
        if not msg:
            raise HTTPException(404, "The message is not found!")
        return await crud.feedback.add(db, models.Feedback(user=current_user, **data.dict()))


# TODO get feedbacks of certain messages
