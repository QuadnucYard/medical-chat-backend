from faker import Faker
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.db.utils import from_orm_async
from app.models import Chat, Feedback, FeedbackRead, MessageCreate, MessageType, User
from app.models.chat import ChatReadWithMessages
from app.models.message import MessageReadWithFeedback
from app.utils.sqlutils import time_now


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
    chat.update_time = time_now()
    await crud.chat.add(db, chat)  # Update time
    await crud.message.create(
        db, MessageCreate(chat_id=chat_id, type=MessageType.Question, content=question)
    )

    fake = Faker("zh_CN")
    ans_txt = fake.text()

    return await crud.message.create(
        db,
        MessageCreate(chat_id=chat_id, type=MessageType.Answer, content=ans_txt),
    )


async def get_chat_with_feedbacks(db: AsyncSession, chat: Chat, user: User):
    def feedback_orm(fb: Feedback | None):
        return FeedbackRead.from_orm(fb) if fb else None

    return await from_orm_async(
        db,
        ChatReadWithMessages,
        chat,
        dict(
            messages=[
                MessageReadWithFeedback.from_orm(
                    msg,
                    dict(own_feedback=feedback_orm(await crud.feedback.get(db, (msg.id, user.id)))),
                )
                for msg in await db.run_sync(lambda _: chat.messages)
            ]
        ),
    )
