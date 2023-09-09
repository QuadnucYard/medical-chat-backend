from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.db.utils import from_orm_async
from app.routers import deps
from app.service import chat_service
from app.utils.sqlutils import is_today, is_yesterday

router = APIRouter()


@router.get("/stat", tags=["stat"])
async def get_chat_stats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    # user: models.User = Depends(deps.get_current_active_superuser),
):
    return {
        "total_chats": await crud.chat.count(db),
        "total_messages": await crud.message.count(db),
        "total_chats_today": await crud.chat.count_if(db, is_today(models.Chat.create_time)),
        "total_messages_today": await crud.message.count_if(db, is_today(models.Message.send_time)),
        "total_chats_yesterday": await crud.chat.count_if(
            db, is_yesterday(models.Chat.create_time)
        ),
        "total_messages_yesterday": await crud.message.count_if(
            db, is_yesterday(models.Message.send_time)
        ),
        "by_date": await chat_service.get_temporal_stats(db),
    }


@router.get("/", response_model=Page[models.ChatRead])
async def get_all_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: deps.PageParams = Depends(),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all chats."""
    return await crud.chat.get_page(db, page=q)


@router.get("/me", response_model=list[models.ChatRead])
async def get_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    """Get chats of current user."""
    chats = await crud.chat.get_by_user(db, user=user)
    return await from_orm_async(db, models.ChatRead, chats)


@router.post("/", response_model=models.ChatRead)
async def create_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.ChatCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create a chat of current user."""
    data.user_id = current_user.id
    chat = await crud.chat.create(db, obj_in=data)
    return await from_orm_async(db, models.ChatRead, chat)


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
    return await chat_service.get_chat_with_feedbacks(db, chat=chat, user=current_user)


@router.put("/{chat_id}", response_model=models.ChatRead)
async def update_title(
    *,
    db: AsyncSession = Depends(deps.get_db),
    chat_id: int,
    data: models.ChatUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    chat = await chat_service.update_title(db, chat_id=chat_id, user=current_user, title=data.title)
    return await from_orm_async(db, models.ChatRead, chat)


@router.post("/{chat_id}", response_model=models.MessageRead)
async def send_question(
    *,
    db: AsyncSession = Depends(deps.get_db),
    chat_id: int,
    question: str = Body(),
    hint: str | None = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return await chat_service.qa(
        db, chat_id=chat_id, question=question, hint=hint, user=current_user
    )


@router.post("/{chat_id}/note", response_model=models.MessageRead)
async def post_note(
    *,
    db: AsyncSession = Depends(deps.get_db),
    chat_id: int,
    data: models.NoteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return await chat_service.create_note(db, chat_id=chat_id, note_in=data, user=current_user)
