import logging
from typing import AsyncGenerator
from uuid import UUID as PyUUID

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    DateTime,
    DECIMAL,
    func
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus

logger = logging.getLogger(__name__)

# Create an async engine for connecting to the database
try:
    engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
    # Create a configured "AsyncSession" class
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    logger.info("Database engine and session maker configured.")
except Exception as e:
    logger.error(f"Failed to configure database engine: {e}", exc_info=True)
    raise

# Base class for our ORM models
Base = declarative_base()


class GenerationRequestORM(Base):
    """
    SQLAlchemy ORM model for the `generation_requests` table.
    This maps to the PostgreSQL table structure defined in SDS Section 7.2.
    """
    __tablename__ = "generation_requests"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    input_parameters = Column(JSONB, nullable=True)
    
    status = Column(String, nullable=False, default=GenerationStatus.PENDING.value, index=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSONB, nullable=True) # Added for more structured error logging
    
    sample_asset_infos = Column(JSONB, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSONB, nullable=True)
    
    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    ai_model_used = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


async def init_db():
    """
    Initializes the database by creating all tables.
    Should be run once on application startup, possibly via a separate script or Alembic.
    """
    async with engine.begin() as conn:
        logger.info("Initializing database, creating tables...")
        # await conn.run_sync(Base.metadata.drop_all) # Use for development/testing only
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created.")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """

    FastAPI dependency to provide a database session.
    This is a redundant definition, the one in `core.dependencies` should be used.
    Keeping it here for structural completeness of the `db_config` module.
    """
    async with SessionLocal() as session:
        yield session