from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_pagination import Page
from app import crud, models
from app.routers import deps

router = APIRouter()


@router.get("/", response_model=Page[models.UserRead])
async def read_users(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: deps.PageParams = Depends(),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Retrieve users.
    """
    return await crud.user.get_page(db, page=q)


@router.post("/", response_model=models.UserRead)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: models.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Create new user.
    """
    user = await crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = await crud.user.create(db, obj_in=user_in)
    """if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )"""
    return user


@router.get("/me", response_model=models.UserRead)
async def read_user_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get current user.
    """
    return await db.run_sync(lambda _: models.UserRead.from_orm(current_user))


@router.put("/me", response_model=models.UserRead)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password: str = Form(None),
    name: str = Form(None),
    email: EmailStr = Form(None),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = models.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if name is not None:
        user_in.name = name
    if email is not None:
        user_in.email = email
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=models.UserRead | None)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Get a specific user by id.
    """
    user = await crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user


@router.put("/{user_id}", response_model=models.UserRead)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: models.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Update a user.
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    return await crud.user.update(db, db_obj=user, obj_in=user_in)
