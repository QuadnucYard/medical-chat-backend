from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.chat import Chat
from app.models.user import User
from app import crud


async def access_chat(db: AsyncSession, chat_id: int, user: User) -> Chat:
    chat = await crud.chat.get(db, chat_id)
    if not crud.chat.is_valid(chat):  # Non-existent or deleted
        raise HTTPException(404, "The chat is not found!")
    if chat.user_id != user.id and not crud.user.is_superuser(user):
        raise HTTPException(403, "You can't access this chat!")
    return chat
