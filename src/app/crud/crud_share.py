from typing import Any, Type
from pydantic import BaseModel
from sqlmodel import select

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.shared_link import SharedLink, SharedLinkCreate
from app.models.user import User, UserCreate, UserUpdate


class CRUDShare(CRUDBase[SharedLink, SharedLinkCreate, BaseModel]):
    ...


share = CRUDShare(SharedLink)
