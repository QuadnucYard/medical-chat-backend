from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps
from app.service import share_service

router = APIRouter()


@router.post("/", response_model=models.SharedLinkRead)
async def create_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.SharedLinkCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create a shared link with unique URL."""
    # The creator must be the chat owner or admin
    # Need chat!
    return await crud.share.create(db, obj_in=data)


@router.delete("/{id}", response_model=models.SharedLinkRead)
async def delete_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: str,
    # current_user: models.User = Depends(deps.get_current_active_user),
):
    "Delete a existent shared link by link. Current user must be the chat owner or admin."
    return await crud.share.remove(db, id=id)


@router.get("/{id}", response_model=models.SharedLinkRead)
async def get_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: str,
    user: models.User | None = Depends(deps.get_current_active_user_opt),
):
    "Request, and try consuming a shared link."
    return await share_service.get_share(db, id, user)


@router.get("/", response_model=Page[models.SharedLinkRead])
async def get_links(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: models.PageParams = Depends(),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    "(Admin) Get all shared links"
    return await crud.share.get_page(db, page=q)
