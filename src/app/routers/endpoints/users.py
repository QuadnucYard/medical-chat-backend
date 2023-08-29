from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.models.user import UserRead
from app.routers import deps

router = APIRouter()

@router.get("/", response_model=models.UserRead)
def read_users(
    db: AsyncSession = Depends(deps.get_db),
    offset: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    return crud.user.gets(db, offset=offset, limit=limit)


@router.get("/me", response_model=UserRead)
def read_user_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
