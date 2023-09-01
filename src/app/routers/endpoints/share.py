from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps

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
):
    "Request, and try consuming a shared link."
    link = await crud.share.get(db, id=id)
    if not link:
        raise HTTPException(403, "This link is not existent!")
    user = await deps.get_current_active_user()
    if not user:
        if link.max_uses != -1:
            raise HTTPException(403, "This link is not existent!")
        return link
    if user in link.user_links:  # User can access links accessed before
        return link
    if link.use_times >= link.max_uses:  # No uses can be offered
        raise HTTPException(403, "This link is not existent!")
    return await crud.share.add_share(db, link, user)


@router.get("/", response_model=list[models.SharedLinkRead])
async def get_links(
    *,
    db: AsyncSession = Depends(deps.get_db),
    offset: int = 0,
    limit: int = 100,
    user: models.User = Depends(deps.get_current_active_superuser),
):
    "(Admin) Get all shared links"
    return await crud.share.gets(db, offset=offset, limit=limit)
