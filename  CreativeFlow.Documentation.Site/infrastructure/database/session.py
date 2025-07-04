```python
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import get_settings

settings = get_settings()

# Create an async engine instance.
# `echo=True` is useful for debugging to see the generated SQL.
# In production, you'd likely set this to False.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

# Create a sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency generator for providing a database session to API endpoints.
    Ensures the session is properly closed after the request is handled.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```