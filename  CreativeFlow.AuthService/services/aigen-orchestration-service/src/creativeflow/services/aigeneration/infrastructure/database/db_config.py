from sqlalchemy import (
    create_engine, MetaData, Table, Column, String, Text, DateTime,
    JSON, DECIMAL
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
import uuid

from creativeflow.services.aigeneration.core.config import settings

# --- SQLAlchemy Async Engine and Session Setup ---
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# --- SQLAlchemy Declarative Base ---
Base = declarative_base()

# --- SQLAlchemy ORM Model for GenerationRequest ---
class GenerationRequestModel(Base):
    """
    SQLAlchemy ORM model that maps to the `generation_requests` table.
    """
    __tablename__ = "generation_requests"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    input_parameters = Column(JSON, nullable=True)
    
    status = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    
    sample_asset_infos = Column(JSON, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSON, nullable=True)
    
    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    
    ai_model_used = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


async def init_db():
    """
    Initializes the database by creating all tables defined by the Base metadata.
    This is useful for development and testing environments.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Use with caution
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """

    FastAPI dependency to provide a new database session for each request.
    """
    async with SessionLocal() as session:
        yield session