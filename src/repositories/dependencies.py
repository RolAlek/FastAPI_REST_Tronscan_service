from contextlib import asynccontextmanager
from typing import AsyncIterable

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from src.application.core.config import settings

engine: AsyncEngine = create_async_engine(url=settings.database.url)
session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncIterable[AsyncSession]:
    async with session_factory.begin() as session:
        yield session


async def get_session_dependency() -> AsyncIterable[AsyncSession]:
    async with session_factory.begin() as session:
        yield session
