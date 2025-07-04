"""
Manages SQLAlchemy database sessions and engine creation.
"""
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)


class DBSessionManager:
    """
    Handles creation of database engine and provides sessions for database
    interaction in an asynchronous context.
    """
    _engine: Optional[AsyncEngine] = None
    _SessionLocal: Optional[async_sessionmaker[AsyncSession]] = None

    @classmethod
    def init_db(cls, database_url: str) -> None:
        """
        Initializes the database engine and session factory.

        This should be called once during application startup.

        Args:
            database_url: The SQLAlchemy database connection string.
        """
        cls._engine = create_async_engine(database_url, echo=False)
        cls._SessionLocal = async_sessionmaker(
            autocommit=False, autoflush=False, bind=cls._engine
        )

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides an AsyncSession in a context manager.

        This is intended to be used as a FastAPI dependency.

        Yields:
            An SQLAlchemy AsyncSession.
        """
        if cls._SessionLocal is None:
            raise IOError("DBSessionManager not initialized. Call init_db() first.")

        async with cls._SessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def close_engine(cls) -> None:
        """Closes the database engine's connection pool."""
        if cls._engine:
            await cls._engine.dispose()
            cls._engine = None
            cls._SessionLocal = None