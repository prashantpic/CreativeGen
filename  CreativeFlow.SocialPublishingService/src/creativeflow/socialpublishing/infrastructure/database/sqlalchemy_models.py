"""
SQLAlchemy ORM models for database tables.
"""
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class SocialConnectionSQL(Base):
    """
    SQLAlchemy ORM model for the 'social_connections' table.
    """

    __tablename__ = "social_connections"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(String, nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    external_user_id = Column(String(255), nullable=False)
    external_display_name = Column(String(255), nullable=True)
    access_token_encrypted = Column(LargeBinary, nullable=False)
    refresh_token_encrypted = Column(LargeBinary, nullable=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
    scopes = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "platform", name="uq_user_platform_connection"),
    )


class PublishJobSQL(Base):
    """

    SQLAlchemy ORM model for the 'publish_jobs' table.
    """

    __tablename__ = "publish_jobs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(String, nullable=False)
    social_connection_id = Column(PG_UUID(as_uuid=True), ForeignKey("social_connections.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    content_text = Column(Text, nullable=True)
    asset_urls = Column(JSON, nullable=True)  # List of strings
    platform_specific_options = Column(JSON, nullable=True)  # Dict
    status = Column(String(50), nullable=False, default="Pending")
    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    published_at = Column(TIMESTAMP(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    attempts = Column(Integer, default=0, nullable=False)
    post_url = Column(String(1024), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_publish_jobs_user_id", "user_id"),
        Index("idx_publish_jobs_status", "status"),
        Index("idx_publish_jobs_scheduled_at", "scheduled_at"),
    )