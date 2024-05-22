from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from application.config import settings


class Base(DeclarativeBase):
    pass


DATABASE_URL: str = settings.db.database_url_asyncpg

engine: AsyncEngine = create_async_engine(DATABASE_URL,
                                          echo=settings.db.ECHO,
                                          echo_pool=settings.db.ECHO_POOL,
                                          pool_size=settings.db.POOL_SIZE,
                                          max_overflow=settings.db.MAX_OVERFLOW)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
