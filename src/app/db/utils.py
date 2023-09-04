from typing import Type, TypeVar
from sqlmodel import SQLModel
from .session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)


async def from_orm_async(db: AsyncSession, model: Type[ModelType], obj: SQLModel) -> ModelType:
    return await db.run_sync(lambda _: model.from_orm(obj))
