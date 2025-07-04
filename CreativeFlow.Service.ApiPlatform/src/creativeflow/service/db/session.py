from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from creativeflow.service.core.config import settings

# Create an asynchronous engine instance using the database URL from settings.
# pool_pre_ping=True helps in handling connections that might have been
# dropped by the database server.
async_engine = create_async_engine(
    settings.DATABASE_URL.render_as_string(hide_password=False),
    pool_pre_ping=True
)

# Create an asynchronous session factory (sessionmaker).
# This factory will be used to create new AsyncSession objects.
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """

    FastAPI dependency that provides an asynchronous database session.

    This function is a generator that yields a new `AsyncSession` for each
    incoming request and ensures it's closed afterward, even if an error occurs.
    The 'async with' statement handles the session's lifecycle automatically.

    Yields:
        An `AsyncSession` object.
    """
    async with AsyncSessionLocal() as session:
        yield session