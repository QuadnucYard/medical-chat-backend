from sqlmodel import SQLModel

from app.models import *
from app import crud, models
from app.core.config import settings
from app.db.session import SessionLocal, engine


async def init_db():
    """Initialize the database and add a default superuser."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    
    async with SessionLocal() as db:
        user = await crud.user.get_by_username(db, username="root")
        if not user:
            user_in = models.UserCreate(
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = await crud.user.create(db, obj_in=user_in)
