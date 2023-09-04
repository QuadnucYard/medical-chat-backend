from typing import Any
from sqlmodel import SQLModel, select

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import Message, MessageRead, MessageCreate


class CRUDMessage(CRUDBase[Message, MessageCreate, SQLModel]):
    ...


message = CRUDMessage(Message)
