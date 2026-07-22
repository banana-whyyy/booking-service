from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from app.modules.auth.models import User, UserRole
from app.modules.auth.crud import get_user
from app.modules.auth.security import decode_jwt 


reusable_oath2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(session: AsyncSession = Depends(get_db), token: str = Depends(reusable_oath2)) -> User:
    cred_exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    try:
        payload = decode_jwt(token)
        user_id = payload["user_id"]
        token_type = payload["type"]
        if token_type != "access":
            raise cred_exceptions
    except (JWTError, ValueError, KeyError):
        raise cred_exceptions
    
    user = await get_user(session, user_id=int(user_id))

    if user is None: 
        raise cred_exceptions

    return user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user