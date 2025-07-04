import logging
from typing import AsyncGenerator
from uuid import UUID as PyUUID

from sqlalchemy import (
    create_engine, MetaData, Column, Table,
    String, Text, DateTime, DECIMAL, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from creativeflow.services.aigeneration.core.config import settings

logger = logging.getLogger(__name__)

# --- SQLAlchemy Async Engine and Session Setup ---
try:
    engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
    SessionLocal = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
except Exception as e:
    logger.critical(f"Failed to create database engine: {e}", exc_info=True)
    raise

# --- Declarative Base and Metadata ---
# Using a common MetaData object is good practice for migrations (e.g., with Alembic)
metadata_obj = MetaData()
Base = declarative_base(metadata=metadata_obj)

# --- SQLAlchemy ORM Model ---
# This class maps to the `generation_requests` table in PostgreSQL.
class GenerationRequestORM(Base):
    __tablename__ = 'generation_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=PyUUID)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    input_parameters = Column(JSONB, nullable=True)
    status = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSONB, nullable=True) # Adding error_details based on domain model
    sample_asset_infos = Column(JSONB, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSONB, nullable=True)
    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    ai_model_used = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# --- Database Initialization (Optional, good for testing/dev) ---
async def init_db():
    """
    Initializes the database by creating all tables.
    Should be used carefully in production (migrations are preferred).
    """
    async with engine.begin() as conn:
        logger.info("Initializing database, creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")

# --- Dependency for getting a DB session (as per SDS) ---
# Note: The actual implementation is in core/dependencies.py to avoid circular imports,
# but the SessionLocal factory is defined and used from here.
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """

    FastAPI dependency to provide a DB session.
    (This is a conceptual duplicate of the one in core/dependencies.py for clarity)
    """
    async with SessionLocal() as session:
        yield session