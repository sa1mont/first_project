from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Генератор асинхронных сессий для FastAPI (Dependency Injection)."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()