"""
SQLAlchemy ORM models for UserProfile service data.

These classes define the database table structures using SQLAlchemy's
declarative mapping, linking Python objects to PostgreSQL tables.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

from sqlalchemy import (JSON, Boolean, DateTime, ForeignKey, String, Text,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class UserProfileSQL(Base):
    """ORM model for the user_profiles table."""
    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    auth_user_id: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    language_preference: Mapped[str] = mapped_column(
        String(10), default="en-US", nullable=False
    )
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    ui_settings: Mapped[Optional[Dict]] = mapped_column(JSON, name="ui_settings_json")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_anonymized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ConsentSQL(Base):
    """ORM model for the user_consents table."""
    __tablename__ = "user_consents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    auth_user_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("user_profiles.auth_user_id"), index=True, nullable=False
    )
    consent_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_granted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        UniqueConstraint('auth_user_id', 'consent_type', name='uq_user_consent_type'),
    )


class DataPrivacyRequestSQL(Base):
    """ORM model for the data_privacy_requests table."""
    __tablename__ = "data_privacy_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    auth_user_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("user_profiles.auth_user_id"), index=True, nullable=False
    )
    request_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    response_data_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)