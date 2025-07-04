"""
db_config.py

Database connection and session management setup using SQLAlchemy.

This module initializes the asynchronous database engine and session factory
for SQLAlchemy. It also defines the ORM models that map to the PostgreSQL
database tables.
"""

import uuid
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import (
    create_engine, Column, String, Text, DateTime, Numeric,
    func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Global Database Variables ---
# These will be initialized by the `init_db` function on application startup.
async_engine = None
AsyncSessionLocal = None

# --- SQLAlchemy Base for ORM models ---
Base = declarative_base()

# --- ORM Model Definition ---

class GenerationRequestORM(Base):
    """
    SQLAlchemy ORM model for the `generation_requests` table.
    This model maps directly to the database schema defined in the SDS.
    """
    __tablename__ = 'generation_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)

    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
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


# --- Database Initialization and Session Management ---

def init_db(database_url: str):
    """
    Initializes the database engine and session factory.
    This function should be called once during the application's startup phase.
    """
    global async_engine, AsyncSessionLocal
    
    async_engine = create_async_engine(database_url, echo=False, pool_pre_ping=True)
    
    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide a database session per request.
    It ensures the session is properly closed after the request is handled.
    """
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() on startup.")
        
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()