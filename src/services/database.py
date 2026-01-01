"""
Database service for handling database operations.
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config.settings import DATABASE_URL
from src.models.base import Base

logger = logging.getLogger(__name__)

# Convert sync URL to async URL if needed
if DATABASE_URL.startswith('sqlite'):
    async_db_url = DATABASE_URL.replace('sqlite://', 'sqlite+aiosqlite://')
elif DATABASE_URL.startswith('postgresql'):
    async_db_url = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
else:
    async_db_url = DATABASE_URL

engine = create_async_engine(async_db_url, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_database():
    """Initialize database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified")


async def get_session() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()