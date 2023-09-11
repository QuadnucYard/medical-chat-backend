from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models


async def get_share(
    db: AsyncSession,
    id: str,
    user: models.User | None,
):
    "Request, and try consuming a shared link."
    link = await crud.share.get(db, id=id)
    if not link:
        raise HTTPException(403, "This link is not existent!")
    # Check expiration
    if crud.share.is_expired(link):
        raise HTTPException(403, "The link has expired!")
    # Check accessibility
    if not user or not user.valid:
        if link.max_uses != -1:
            raise HTTPException(403, "You can't access this link!")
        return link
    # Check whether the user is the owner
    if await crud.share.is_user_shared(db, user.id, id):  # User can access links accessed before
        return link
    if link.use_times >= link.max_uses:  # No uses can be offered
        raise HTTPException(403, "This link is exhausted!")
    return await crud.share.add_share(db, link, user)
