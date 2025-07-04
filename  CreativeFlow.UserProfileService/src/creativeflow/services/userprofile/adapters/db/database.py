"""
SQLAlchemy database connection and session management.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from ...config import get_settings

settings = get_settings()

# Create the asynchronous engine from the database URL in settings
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # Log SQL statements in dev
)

# Create a configured "Session" class for creating new session objects
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Create a base class for declarative class definitions (our ORM models)
Base = declarative_base()


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency provider for FastAPI that yields an SQLAlchemy AsyncSession.

    This function creates a new session for each request, yields it to the
    endpoint, and ensures it's closed afterward.
    """
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_and_tables():
    """
    Creates all database tables defined by the Base metadata.
    This is useful for initial setup or testing environments.
    It should not be used for migrations in a production environment.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)