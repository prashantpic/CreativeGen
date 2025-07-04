import logging
from typing import AsyncGenerator

from sqlalchemy import (Column, DateTime, MetaData, Numeric, String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

from creativeflow.services.aigeneration.core.config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy engine
try:
    engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
except Exception as e:
    logger.error("Failed to create database engine: %s", e)
    engine = None

# SQLAlchemy session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base for declarative models
Base = declarative_base()


# --- ORM Model for the generation_requests table ---
class GenerationRequestOrm(Base):
    """
    SQLAlchemy ORM model corresponding to the 'generation_requests' table.
    """
    __tablename__ = "generation_requests"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    
    # All other input parameters are stored in a flexible JSONB field
    input_parameters = Column(JSONB, nullable=True)
    
    status = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    
    sample_asset_infos = Column(JSONB, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSONB, nullable=True)
    
    credits_cost_sample = Column(Numeric(10, 4), nullable=True)
    credits_cost_final = Column(Numeric(10, 4), nullable=True)
    
    ai_model_used = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# --- Database Session Dependency ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide an async DB session.
    """
    async with SessionLocal() as session:
        yield session

async def init_db():
    """
    Initializes the database and creates tables if they don't exist.
    Should be called on application startup.
    """
    if not engine:
        logger.critical("Database engine is not initialized. Cannot create tables.")
        return
        
    async with engine.begin() as conn:
        logger.info("Creating database tables...")
        # Use run_sync to create tables. This is a one-time operation.
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully.")