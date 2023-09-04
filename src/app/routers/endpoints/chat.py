from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps

router = APIRouter()


@router.post("/", response_model=models.ChatRead)
async def create_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.ChatCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create a chat of current user."""
    data.user_id = current_user.id
    return await crud.chat.create(db, obj_in=data)


@router.delete("/{id}", response_model=str)
async def delete_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    "Delete a chat. The operator must be the chat owner of superuser."
    chat = await crud.chat.get(db, id)
    if not crud.chat.is_valid(chat):  # Non-existent or deleted
        raise HTTPException(404, "The chat is not found!")
    if chat.user_id != current_user.id and not crud.user.is_superuser(current_user):
        raise HTTPException(403, "You can't delete this chat!")
    await crud.chat.delete(db, chat)
    return "Successfully deleted the chat."


@router.get("/", response_model=list[models.ChatRead])
async def get_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    "Get chats of current user"
    return await crud.chat.get_by_user(db, user=user)


"""

@router.get("/{id}", response_model=models.ChatReadWithMessages)
async def get_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    "Get chats of current"
    link = await crud.share.get(db, id=id)
    if not link:
        raise HTTPException(403, "This link is not existent!")
    if crud.share.is_expired(link):
        raise HTTPException(403, "The link has expired!")
    if not user or not user.valid:
        if link.max_uses != -1:
            raise HTTPException(403, "You can't access this link!")
        return link
    # Check whether the user is the owner 
    if await crud.share.is_user_shared(db, user.id, id):  # User can access links accessed before
        return link
    if link.use_times >= link.max_uses:  # No uses can be offered
        raise HTTPException(403, "This link is exhausted!")
    # TODO more checks: valid, expire
    return await crud.share.add_share(db, link, user)


@router.get("/", response_model=list[models.SharedLinkRead])
async def get_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    offset: int = 0,
    limit: int = 100,
    user: models.User = Depends(deps.get_current_active_superuser),
):
    "(Admin) Get all shared links"
    return await crud.share.gets(db, offset=offset, limit=limit)


"""
