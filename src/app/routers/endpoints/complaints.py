from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps
from app.utils.sqlutils import time_now

router = APIRouter()


@router.get("/", response_model=Page[models.ComplaintReadDetailed])
async def get_complaints(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: deps.PageParams = Depends(),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all feedbacks."""
    return await crud.complaint.get_page(db, page=q)


@router.post("/", response_model=models.ComplaintRead)
async def create_complaint(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.ComplaintCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create complaint."""
    return await crud.complaint.add(db, models.Complaint(content=data.content, user=current_user))


@router.post("/{id}", response_model=models.ComplaintRead)
async def resolve_complaint(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """Resolve a complaint."""
    complaint = await crud.complaint.get(db, id)
    if not complaint:
        raise HTTPException(404, "The complaint is not found!")
    
    complaint.admin = current_user
    complaint.resolve_time = time_now()

    return await crud.complaint.add(db, complaint)
