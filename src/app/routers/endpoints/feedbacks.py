from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps

router = APIRouter()


@router.get("/", response_model=list[models.FeedbackRead])
async def get_feedbacks(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: deps.QueryParams = Depends(),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all feedbacks."""
    return await crud.feedback.gets(db, offset=q.offset, limit=q.limit)


@router.post("/", response_model=models.FeedbackRead)
async def update_feedback(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.FeedbackUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Update feedback of the user. Create feedback if necessary."""
    data.user_id = current_user.id
    return await crud.feedback.create(db, obj_in=data)


# TODO get feedbacks of certain messages
