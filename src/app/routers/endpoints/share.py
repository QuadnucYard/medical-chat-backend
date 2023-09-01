

from datetime import datetime, timezone
from fastapi import APIRouter, Body, Depends, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, models
from app.models.shared_link import SharedLinkRead
from app.routers import deps

router = APIRouter()


@router.post("/", response_model=models.SharedLinkRead)
async def create_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.SharedLinkCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create a shared link with unique URL."""
    return await crud.share.create(db, obj_in=data)
