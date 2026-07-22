from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import UTC, datetime

from app.modules.auth.crud import(
    get_user_by_email,
    get_user_by_username,
    create_user,
    get_refresh_token,
    register_refresh_token_db,
    delete_all_user_refresh_tokens
)
from app.modules.auth.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.modules.auth.security import create_access_token, create_refresh_token, verify_password, decode_jwt
from app.database import get_db



router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already register",
        )
    
    if await get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already register",
        )
    
    new_user = await create_user(db, user)
    
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_payload = {"user_id": user.id, "type": "access"}
    access_token = create_access_token(data=access_payload)

    refresh_payload = {"user_id": user.id, "type": "refresh"}
    refresh_token = create_refresh_token(data=refresh_payload)

    await register_refresh_token_db(db, token=refresh_token, user_id=user.id)
    await db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    token = await get_refresh_token(db, refresh_token)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    payload = decode_jwt(token.token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token type"
        )
    
    if token.is_used:
        async with db.begin():
            await delete_all_user_refresh_tokens(db, user_id=token.user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security alert. Session compromised"
        )
    
    new_payload = {"sub": str(token.user_id)}
    token.is_used = True

    token.used_at = datetime.now(UTC)
    access_token = create_access_token(data=new_payload)
    new_refresh_token = create_refresh_token(data=new_payload)

    await register_refresh_token_db(db, token=new_refresh_token, user_id=token.user_id)
    await db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
