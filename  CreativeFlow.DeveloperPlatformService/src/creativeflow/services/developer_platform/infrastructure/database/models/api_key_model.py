from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class APIKeyModel(Base):
    """
    SQLAlchemy ORM model representing the 'api_keys' table in the database.

    This table stores developer API keys, including a hashed secret, permissions,
    and lifecycle status.
    """

    __tablename__ = "api_keys"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        # ForeignKey("users.id"), # This would be a real FK to a users table
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    secret_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    permissions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    usage_records = relationship("UsageRecordModel", back_populates="api_key")
    quota = relationship("QuotaModel", back_populates="api_key", uselist=False)

    def __repr__(self) -> str:
        return f"<APIKeyModel(id={self.id}, name='{self.name}', user_id='{self.user_id}')>"