from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import NotFoundHTTPException, BadRequestHTTPException
from ..db import get_db
from .auth import is_connected, get_password_hash
from ..models.user import User
from ..schemas.user import UserSchema, UserResponse, UsersResponse


router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(is_connected)],
)


@router.get("/me", response_model=UserResponse)
async def get_current_user(user: User = Depends(is_connected)):
    """Provides information about the user logged in."""
    return user


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: UUID, db_session: AsyncSession = Depends(get_db)):
    """Provides information about an user."""
    user = await User.find(db_session, id)
    if not user:
        raise NotFoundHTTPException()

    return user


@router.put("/{id}", response_model=UserResponse)
async def update_user(id: UUID, payload: UserSchema, db_session: AsyncSession = Depends(get_db)):
    hashed_pwd = get_password_hash(payload.password)

    user = await User.find(db_session, id)
    await user.update(db_session, **payload.dict(), hashed_password=hashed_pwd)

    return user


@router.delete("/{id}", response_model=UserResponse)
async def delete_user(id: UUID, user: User = Depends(is_connected), db_session: AsyncSession = Depends(get_db)):
    if user.id == id:
        raise BadRequestHTTPException("You can't delete your own user.")

    user = await User.find(db_session, id)
    await user.delete(db_session)

    return user


@router.post("", response_model=UserResponse)
async def create_user(payload: UserSchema, db_session: AsyncSession = Depends(get_db)):
    hashed_pwd = get_password_hash(payload.password)

    if await User.from_username_email(db_session, payload.username, payload.email):
        raise BadRequestHTTPException("That username or email is already in use")
    user = User(**payload.dict(), hashed_password=hashed_pwd)
    await user.save(db_session)

    return user


@router.get("", response_model=UsersResponse)
async def get_users(
    limit: Optional[int] = Query(10, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
    db_session: AsyncSession = Depends(get_db),
):
    count, page = await User.all(db_session, limit, offset)

    return {
        "offset": offset,
        "limit": limit,
        "results": page,
        "total": count,
    }
