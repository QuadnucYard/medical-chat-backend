from typing import Any, Type, TypeVar
from sqlmodel import SQLModel
from .session import AsyncSession, AsyncEngine

ModelType = TypeVar("ModelType", bound=SQLModel)


async def from_orm_async(
    db: AsyncSession, model: Type[ModelType], obj: SQLModel, update: dict[str, Any] | None = None
) -> ModelType:
    return await db.run_sync(lambda _: model.from_orm(obj, update))


class no_echo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.echo = self.engine.echo

    def __enter__(self):
        self.echo = self.engine.echo
        self.engine.echo = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.echo = self.echo
