import logging
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ....developer_platform.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

try:
    # Create the async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.LOG_LEVEL.upper() == "DEBUG",  # Log SQL queries in debug mode
    )

    # Create a session maker
    AsyncSessionLocal = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
except Exception as e:
    logger.exception("Failed to initialize database engine and session maker.")
    raise e


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """

    FastAPI dependency that provides an asynchronous database session.

    This function is a generator that yields a new SQLAlchemy `AsyncSession`
    for each request. It ensures that the session is always closed after the
    request is finished, even if an error occurs.

    Yields:
        An `AsyncSession` object.
    """
    session: AsyncSession = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database transaction failed: {e}")
        await session.rollback()
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during DB session: {e}")
        await session.rollback()
        raise
    finally:
        await session.close()