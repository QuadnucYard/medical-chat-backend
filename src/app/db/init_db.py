import random
from typing import Any
from faker import Faker
from sqlmodel import SQLModel

from app.models import *
from app import crud
from app.core.config import settings
from app.db.session import SessionLocal, engine, AsyncSession


class Init:
    def __init__(self) -> None:
        self.users = list[User]()
        self.chats = list[Chat]()
        self.fake = Faker("zh_CN")

    async def init_perms(self, db: AsyncSession):
        perm1 = await crud.perm.create(db, PermCreate(name="Chat access", desc="", route=""))
        perm2 = await crud.perm.create(db, PermCreate(name="User management", desc="", route=""))
        perm3 = await crud.perm.create(db, PermCreate(name="KB management", desc="", route=""))
        RoleCreate.update_forward_refs()
        role1 = await crud.role.add(db, Role(name="Normal User", perms=[perm1]))
        role2 = await crud.role.add(db, Role(name="Super User", perms=[perm1, perm2, perm3]))
        self.role_norm = role1
        self.role_super = role2

    async def init_users(self, db: AsyncSession, num: int):
        self.users.append(
            await crud.user.create(
                db,
                obj_in=UserCreate(
                    username=settings.FIRST_SUPERUSER,
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    is_superuser=True,
                    role_id=self.role_super.id,
                ),
            )
        )

    async def init_chats(self, db: AsyncSession, num: int):
        superuser = self.users[0]
        self.chats = [
            await crud.chat.add(db, Chat(user=superuser, title=self.fake.sentence()))
            for _ in range(num)
        ]

    async def init_messages(self, db: AsyncSession, num: int):
        self.messages = [
            await crud.message.add(
                db,
                Message(
                    chat=random.choice(self.chats),
                    type=random.choice(list(MessageType)),
                    content=self.fake.text(),
                ),
            )
            for _ in range(num)
        ]

    async def init_feedbacks(self, db: AsyncSession, num: int):
        superuser = self.users[0]
        msg_samples = random.sample(self.messages, num)
        self.feedbacks = [
            await crud.feedback.add(
                db,
                Feedback(
                    user=superuser,
                    msg=msg,
                    mark_like=random.choices((True, False), (0.5, 0.5))[0],
                    mark_dislike=random.choices((True, False), (0.3, 0.7))[0],
                    content=self.fake.sentence() if random.random() < 0.2 else "",
                ),
            )
            for msg in msg_samples
        ]

    async def __call__(self, db: AsyncSession):
        await self.init_perms(db)
        await self.init_users(db, 0)
        await self.init_chats(db, 10)
        await self.init_messages(db, 100)
        await self.init_feedbacks(db, 50)


async def init_db():
    """Initialize the database and add a default superuser."""
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        
    async with SessionLocal() as db:
        user = await crud.user.get_by_username(db, username="root")
        if not user:
            ini = Init()
            await ini(db)
