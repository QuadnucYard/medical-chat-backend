from sqlmodel import SQLModel

from app.models import *
from app import crud, models
from app.core.config import settings
from app.db.session import SessionLocal, engine


async def init_db():
    """Initialize the database and add a default superuser."""
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with SessionLocal() as db:
        user = await crud.user.get_by_username(db, username="root")
        if not user:
            perm1 = await crud.perm.create(db, PermCreate(name="Chat access", desc="", route=""))
            perm2 = await crud.perm.create(
                db, PermCreate(name="User management", desc="", route="")
            )
            perm3 = await crud.perm.create(db, PermCreate(name="KB management", desc="", route=""))
            RoleCreate.update_forward_refs()
            role1 = await crud.role.add(db, Role(name="Normal User", perms=[perm1]))
            role2 = await crud.role.add(db, Role(name="Super User", perms=[perm1, perm2, perm3]))

            user = await crud.user.create(
                db,
                obj_in=UserCreate(
                    username=settings.FIRST_SUPERUSER,
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    is_superuser=True,
                    role_id=role2.id,
                ),
            )

        chat = Chat(user=user, title="")
        db.add(chat)
        await db.commit()
        await db.refresh(chat)

        # db.expire(user)
        # await db.refresh(user, ["role"])
        # all_roles = (await db.scalars(user.role.statement)).all()
        # print(all_roles)
        # print(user.role)
        # print(await db.run_sync(lambda _: user.role))
        # print("llll", user.role)
