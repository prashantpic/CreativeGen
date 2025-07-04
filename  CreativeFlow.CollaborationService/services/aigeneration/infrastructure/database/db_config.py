import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    DateTime,
    String,
    Text,
    DECIMAL,
    func
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
import uuid

from creativeflow.services.aigeneration.core.config import settings

logger = logging.getLogger(__name__)

# --- SQLAlchemy Setup ---
try:
    engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
    SessionLocal = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
except Exception as e:
    logger.critical(f"Failed to initialize database engine: {e}", exc_info=True)
    engine = None
    SessionLocal = None

# --- Base Model ---
class Base(DeclarativeBase):
    pass

# --- ORM Model for GenerationRequest ---
class GenerationRequestOrm(Base):
    __tablename__ = "generation_requests"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    
    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    ai_model_used = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# --- Dependency for DB Session ---
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide a database session.
    Ensures the session is closed after the request.
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. SessionLocal is None.")
        
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initializes the database, creating tables if they don't exist.
    Should be called on application startup.
    """
    if engine is None:
        logger.error("Database engine is not available. Cannot initialize DB.")
        return
        
    async with engine.begin() as conn:
        # In a production environment, you would use Alembic for migrations.
        # This is suitable for development and testing.
        logger.info("Initializing database and creating tables...")
        # await conn.run_sync(Base.metadata.drop_all) # Use for clean slate in dev
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully.")