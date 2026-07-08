from datetime import timedelta, datetime, UTC
from jose import JWTError, jwt

from passlib.context import CryptContext
from app.config import settings


ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def encode_jwt(
        data: dict,
        token_type: str,
        expires_delta: timedelta | None = None,
        algorithm: str = settings.algorithm,
        secret_key: str = settings.secret_key,
) -> str:
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=15)
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    encoded = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str,
        algorithm: str = settings.algorithm,
        secret_key: str = settings.secret_key,
) -> dict:
    return jwt.decode(token, secret_key, algorithms=[algorithm])


def create_access_token(data: dict) -> str:
    return encode_jwt(
        data=data,
        token_type=ACCESS_TOKEN_TYPE,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )


def create_refresh_token(data: dict) -> str:
    return encode_jwt(
        data=data,
        token_type=REFRESH_TOKEN_TYPE,
        expires_delta=timedelta(days=settings.refresh_token_expire_days)
    )