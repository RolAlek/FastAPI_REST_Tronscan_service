import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from aioinject import Container, Scoped
from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from application.api.app import create_app
from application.core.config import BASE_DIR
from application.di.container import init_container
from domain.models import Base
from repositories.modules.wallet.repository import _WalletRepository
from services.tron.service import _TronService
from services.wallet.service import WalletService

TEST_DB_PATH = BASE_DIR / "test.db"
TEST_DB_URL = f"sqlite+aiosqlite:///{TEST_DB_PATH}"


engine: AsyncEngine = create_async_engine(TEST_DB_URL, echo=True)
session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
    os.remove(TEST_DB_PATH)


@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory.begin() as session:
        yield session


@asynccontextmanager
async def test_session_dependency() -> AsyncGenerator[AsyncSession]:
    async with session_factory.begin() as session:
        yield session


@pytest.fixture
def init_test_container() -> Container:
    container = init_container()
    container.try_register(Scoped(test_session_dependency, type_=AsyncSession))
    return container


@pytest.fixture
def wallet_service(test_session: AsyncSession):
    repo = _WalletRepository(session=test_session)
    tron_mock = _TronService(AsyncMock())
    service = WalletService(service=tron_mock, repository=repo)
    return service, tron_mock


@pytest.fixture
def app(init_test_container) -> FastAPI:
    app = create_app()
    app.add_middleware(AioInjectMiddleware, container=init_test_container)
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
