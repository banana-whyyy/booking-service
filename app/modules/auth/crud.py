from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import timezone, datetime, timedelta

from app.modules.auth.models import User, RefreshToken
from app.modules.auth.schemas import UserCreate
from app.modules.auth.security import get_password_hash
from app.config import settings


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.flush()
    return db_user


async def register_refresh_token_db(db: AsyncSession, token: str, user_id: int) -> RefreshToken:
    expire_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    db_refresh = RefreshToken(
        user_id=user_id,
        expires_at=expire_at,
        token=token
    )

    db.add(db_refresh)
    await db.flush()
    await db.commit()
    await db.refresh(db_refresh)
    return db_refresh


async def get_refresh_token(db: AsyncSession, token: str) -> RefreshToken | None:
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token).with_for_update()
    )
    return result.scalar_one_or_none()


async def delete_all_user_refresh_tokens(db: AsyncSession, user_id: int):
    await db.execute(
        delete(RefreshToken).where(RefreshToken.user_id == user_id)
    )