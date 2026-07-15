from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer 
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, get_db
from app.config import settings
from auth.models import User 
from auth.security import decode_jwt 


reusable_oath2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oath2)]

async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    cred_exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    try:
        payload = decode_jwt(token)
        user_id = payload["user_id"]
        token_type = payload["type"]
        if token_type != "access":
            raise cred_exceptions
    except (JWTError, ValueError):
        raise cred_exceptions
    
    result = await session.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalars().first()

    if user is None: 
        raise cred_exceptions

    return user
