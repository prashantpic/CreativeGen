from sqlalchemy import (
    create_engine, Column, String, Text, DateTime,
    ForeignKey, DECIMAL
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

from ...core.config import settings

# --- SQLAlchemy Async Engine and Session Setup ---

# Create an asynchronous engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, # Set to True to see generated SQL statements
    pool_pre_ping=True
)

# Create a configured "Session" class
# Use this to create new sessions for each request
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    class_=AsyncSession
)

# Dependency to get a DB session in FastAPI endpoints
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# --- Base for ORM Models ---
Base = declarative_base()

# --- ORM Model for the generation_requests table ---

class GenerationRequestModel(Base):
    """
    SQLAlchemy ORM model for the 'generation_requests' table.
    This maps directly to the database table schema defined in the SDS.
    """
    __tablename__ = 'generation_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    
    # Store the full original request for auditing and regeneration purposes
    input_parameters = Column(JSONB, nullable=True)
    
    status = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSONB, nullable=True) # For storing structured error data from n8n

    # Store lists of asset info objects as JSON arrays
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
    (Optional) A function to create all tables in the database.
    In a production setup, this is typically handled by a migration tool like Alembic.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Use with caution
        await conn.run_sync(Base.metadata.create_all)