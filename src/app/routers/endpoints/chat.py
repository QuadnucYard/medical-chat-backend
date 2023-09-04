from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.db.utils import from_orm_async
from app.routers import deps
from app.service import chat_service

router = APIRouter()


@router.get("/", response_model=list[models.ChatRead])
async def get_all_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    offset: int = 0,
    limit: int = 100,
    user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all chats."""
    return await crud.chat.gets(db, offset=offset, limit=limit)


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
    """Delete a chat. The operator must be the chat owner of superuser."""
    chat = await chat_service.access_chat(db, chat_id=id, user=current_user)
    chat.delete_time = datetime.now()
    await crud.chat.add(db, chat)
    return "Successfully deleted the chat."


@router.get("/{id}", response_model=models.ChatReadWithMessages)
async def get_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Get chat contents."""
    chat = await chat_service.access_chat(db, chat_id=id, user=current_user)
    return await from_orm_async(db, models.ChatReadWithMessages, chat)


@router.get("/me", response_model=list[models.ChatRead])
async def get_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    """Get chats of current user."""
    return await crud.chat.get_by_user(db, user=user)
