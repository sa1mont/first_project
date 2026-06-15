import asyncio
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings


engine_test = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="function", autouse=True)
async def clean_database():
    """Перед каждым тестом очищает базу данных и создает чистые таблицы."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine_test.dispose()

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Подменяет реальную сессию БД на тестовую."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Асинхронный клиент для отправки HTTP-запросов к нашему приложению."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client