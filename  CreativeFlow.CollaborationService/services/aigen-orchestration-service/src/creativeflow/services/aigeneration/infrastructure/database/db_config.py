import logging
from typing import AsyncGenerator
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Text,
    DateTime,
    func,
    DECIMAL,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from creativeflow.services.aigeneration.core.config import settings

logger = logging.getLogger(__name__)

# --- SQLAlchemy ORM Setup ---
# Using ORM allows for easier mapping and less raw SQL.
Base = declarative_base()

class GenerationRequestOrm(Base):
    """
    SQLAlchemy ORM model for the 'generation_requests' table.
    This maps directly to the database schema.
    """
    __tablename__ = "generation_requests"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    input_parameters = Column(JSONB, nullable=True)
    status = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSONB, nullable=True)
    sample_asset_infos = Column(JSONB, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSONB, nullable=True)
    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    ai_model_used = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# --- Async Database Engine and Session ---
try:
    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    SessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    logger.info("Successfully created async database engine and session maker.")
except Exception as e:
    logger.critical(f"Failed to create database engine: {e}", exc_info=True)
    # The application should not start if the DB can't be configured.
    raise

async def init_db():
    """
    Initializes the database by creating all tables defined by the ORM models.
    This is useful for development and testing. For production, migrations (e.g., Alembic)
    are recommended.
    """
    async with engine.begin() as conn:
        logger.info("Initializing database tables...")
        # await conn.run_sync(Base.metadata.drop_all) # Use for clean slate in dev
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide a database session per request.
    """
    async with SessionLocal() as session:
        yield session