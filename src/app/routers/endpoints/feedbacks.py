from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps

router = APIRouter()


@router.get("/", response_model=Page[models.FeedbackReadWithMsgUser])
async def get_feedbacks(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: deps.PageParams = Depends(),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all feedbacks."""
    return await crud.feedback.get_page(db, page=q)


@router.put("/", response_model=models.FeedbackRead)
async def update_feedback(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.FeedbackUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Update feedback of the user. Create feedback if necessary."""
    if data.mark_like and data.mark_dislike:
        data.mark_like = False  # Exclusive
    fb = await crud.feedback.get(db, (data.msg_id, current_user.id))
    if fb:
        fb.update_time = datetime.now()
        return await crud.feedback.update(db, db_obj=fb, obj_in=data)
        # 暂时不做互斥了……
    else:
        msg = await crud.message.get(db, data.msg_id)
        if not msg:
            raise HTTPException(404, "The message is not found!")
        return await crud.feedback.add(db, models.Feedback(user=current_user, **data.dict()))


# TODO get feedbacks of certain messages
