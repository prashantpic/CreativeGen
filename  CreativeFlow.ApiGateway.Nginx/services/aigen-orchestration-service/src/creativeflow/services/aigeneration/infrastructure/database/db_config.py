import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import (
    create_engine, Column, String, DateTime, Text, JSON, DECIMAL
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus

# --- SQLAlchemy ORM Model Definition ---

Base = declarative_base()

class GenerationRequestOrm(Base):
    """
    SQLAlchemy ORM model for the `generation_requests` table.
    This maps the database table to a Python class.
    """
    __tablename__ = "generation_requests"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)

    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    
    # Store all other input params in a single JSONB column for flexibility
    input_parameters = Column(JSON, nullable=True) 

    status = Column(String, nullable=False, default=GenerationStatus.PENDING.value, index=True)
    error_message = Column(Text, nullable=True)

    sample_asset_infos = Column(JSON, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSON, nullable=True)

    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    ai_model_used = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# --- Database Engine and Session Configuration ---

# Create an asynchronous engine
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Create a configured "Session" class
# Use AsyncSession for the session class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    """
    Initializes the database by creating all tables defined by the Base metadata.
    This is useful for development and testing. For production, migrations (e.g., with Alembic)
    are recommended.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Use with caution in dev
        await conn.run_sync(Base.metadata.create_all)