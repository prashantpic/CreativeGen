```python
import uuid
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import (
    create_engine, Column, String, Text, DateTime,
    DECIMAL, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from creativeflow.services.aigeneration.core.config import settings

# --- SQLAlchemy ORM Model Definition ---

Base = declarative_base()

class GenerationRequestOrm(Base):
    """
    SQLAlchemy ORM model for the 'generation_requests' table.
    """
    __tablename__ = "generation_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    input_parameters = Column(JSON, nullable=True)
    status = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True) # For structured errors
    sample_asset_infos = Column(JSON, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSON, nullable=True)
    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    ai_model_used = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# --- Database Session Management ---

# Create an async engine instance.
async_engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker for creating async sessions.
AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=async_engine, 
    class_=AsyncSession
)

async def init_db():
    """
    Initializes the database by creating all tables.
    Should be called on application startup.
    In a production environment, this would be handled by a migration tool like Alembic.
    """
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Uncomment for easy reset during dev
        await conn.run_sync(Base.metadata.create_all)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide a DB session per request.
    """
    async with AsyncSessionLocal() as session:
        yield session
```