import logging
from typing import AsyncGenerator

from sqlalchemy import (
    create_engine, MetaData, Table, Column, String, Text, DateTime,
    JSON, Uuid, DECIMAL, func
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher

logger = logging.getLogger(__name__)

# --- Database Setup ---
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,

    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# --- SQLAlchemy ORM Model ---
class GenerationRequestModel(Base):
    __tablename__ = 'generation_requests'

    id = Column(Uuid, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    project_id = Column(String, nullable=False, index=True)
    input_prompt = Column(Text, nullable=False)
    style_guidance = Column(Text, nullable=True)
    input_parameters = Column(JSON, nullable=True)
    status = Column(String, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    sample_asset_infos = Column(JSON, nullable=True)
    selected_sample_id = Column(String, nullable=True)
    final_asset_info = Column(JSON, nullable=True)
    credits_cost_sample = Column(DECIMAL, nullable=True)
    credits_cost_final = Column(DECIMAL, nullable=True)
    ai_model_used = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


async def init_db():
    """Initializes the database and creates tables if they don't exist."""
    async with engine.begin() as conn:
        logger.info("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created (if not existed).")

# --- RabbitMQ Global Instance ---
rabbitmq_publisher_instance: RabbitMQPublisher | None = None

async def init_rabbitmq():
    """Initializes the global RabbitMQ publisher instance."""
    global rabbitmq_publisher_instance
    logger.info("Initializing RabbitMQ publisher...")
    rabbitmq_publisher_instance = RabbitMQPublisher(settings.RABBITMQ_URL)
    await rabbitmq_publisher_instance.connect()
    logger.info("RabbitMQ publisher connected.")

async def close_rabbitmq():
    """Closes the global RabbitMQ publisher connection."""
    global rabbitmq_publisher_instance
    if rabbitmq_publisher_instance:
        logger.info("Closing RabbitMQ publisher connection...")
        await rabbitmq_publisher_instance.close()
        logger.info("RabbitMQ publisher connection closed.")