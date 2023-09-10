import aiohttp
from faker import Faker
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.core.config import settings
from app.db.utils import from_orm_async
from app.models import Chat, Feedback, FeedbackRead, MessageCreate, MessageType, User
from app.models.chat import ChatReadWithMessages
from app.models.message import MessageReadWithFeedback, NoteCreate
from app.utils.sqlutils import time_now
from app.utils.statutils import counter_helper


async def access_chat(
    db: AsyncSession,
    chat_id: int,
    user: User,
    *,
    allow_admin: bool = True,
    update_time: bool = False
) -> Chat:
    chat = await crud.chat.get(db, chat_id)
    if not crud.chat.is_valid(chat):  # Non-existent or deleted
        raise HTTPException(404, "The chat is not found!")
    if not (chat.user_id == user.id or allow_admin and crud.user.is_superuser(user)):
        raise HTTPException(403, "You can't access this chat!")
    if update_time:
        await update_chat_time(db, chat)
    return chat


async def update_chat_time(db: AsyncSession, chat: Chat) -> Chat:
    chat.update_time = time_now()
    return await crud.chat.add(db, chat)


async def qa(db: AsyncSession, chat_id: int, question: str, hint: str | None, user: User):
    chat = await access_chat(db, chat_id=chat_id, user=user, allow_admin=False, update_time=True)

    question_msg = await crud.message.create(
        db,
        MessageCreate(
            chat_id=chat_id, type=MessageType.Question, content=question, remark=hint or ""
        ),
    )

    if settings.ENABLE_KGQA:
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.KGQA_API, data=question) as response:
                obj = await response.json()
                ans_txt = obj["answer"]
    else:
        fake = Faker("zh_CN")
        ans_txt: str = fake.text()

    answer_msg = await crud.message.create(
        db,
        MessageCreate(chat_id=chat_id, type=MessageType.Answer, content=ans_txt, remark=""),
    )
    return [question_msg, answer_msg]


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


async def update_title(db: AsyncSession, chat_id: int, user: User, title: str):
    chat = await access_chat(db, chat_id=chat_id, user=user)
    chat.title = title
    chat.update_time = time_now()
    return await crud.chat.add(db, chat)


async def create_note(db: AsyncSession, chat_id: int, note_in: NoteCreate, user: User):
    await access_chat(db, chat_id=chat_id, user=user)

    return await crud.message.create(
        db,
        MessageCreate(
            chat_id=chat_id, type=MessageType.Note, content=note_in.content, remark=note_in.remark
        ),
    )


async def get_temporal_stats(db: AsyncSession):
    return await counter_helper(
        db,
        (crud.chat.count_by_date, "total_chats"),
        (crud.message.count_by_date, "total_messages"),
        (crud.message.count_q_by_date, "questions"),
        (crud.message.count_a_by_date, "answers"),
        (crud.message.count_n_by_date, "notes"),
    )
