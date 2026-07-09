from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator
from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


class Base(DeclarativeBase):
    pass


# в проде поменять на echo=False
engine = create_async_engine(settings.database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:        
        yield session