from faker import Faker
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.chat import Chat
from app.models.message import MessageCreate, MessageType
from app.models.user import User
from app import crud


async def access_chat(
    db: AsyncSession, chat_id: int, user: User, *, allow_admin: bool = True
) -> Chat:
    chat = await crud.chat.get(db, chat_id)
    if not crud.chat.is_valid(chat):  # Non-existent or deleted
        raise HTTPException(404, "The chat is not found!")
    if not (chat.user_id == user.id or allow_admin and crud.user.is_superuser(user)):
        raise HTTPException(403, "You can't access this chat!")
    return chat


async def qa(db: AsyncSession, chat_id: int, question: str, hint: str | None, user: User):
    chat = await access_chat(db, chat_id=chat_id, user=user, allow_admin=False)
    await crud.message.create(
        db, MessageCreate(chat_id=chat_id, type=MessageType.Question, content=question)
    )

    fake = Faker("zh_CN")
    ans_txt = fake.text()

    return await crud.message.create(
        db,
        MessageCreate(chat_id=chat_id, type=MessageType.Answer, content=ans_txt),
    )
