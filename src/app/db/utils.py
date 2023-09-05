from typing import Any, Type, TypeVar
from sqlmodel import SQLModel
from .session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)


async def from_orm_async(
    db: AsyncSession, model: Type[ModelType], obj: SQLModel, update: dict[str, Any] | None = None
) -> ModelType:
    return await db.run_sync(lambda _: model.from_orm(obj, update))
