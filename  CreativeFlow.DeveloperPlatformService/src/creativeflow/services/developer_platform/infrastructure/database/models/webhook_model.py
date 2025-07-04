from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class WebhookModel(Base):
    """
    SQLAlchemy ORM model representing the 'webhooks' table.

    This table stores developer-configured webhook endpoints, their subscribed
    event types, and an optional hashed secret for signature verification.
    """

    __tablename__ = "webhooks"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        # ForeignKey("users.id"), # This would be a real FK to a users table
        index=True,
        nullable=False,
    )
    target_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    event_types: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    hashed_secret: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )

    def __repr__(self) -> str:
        return f"<WebhookModel(id={self.id}, target_url='{self.target_url}', user_id='{self.user_id}')>"