import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Webhook(Base):
    """
    SQLAlchemy ORM model for a Webhook.

    Represents a developer-registered URL to receive notifications for specific events.
    """
    __tablename__ = "Webhook"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    api_client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("APIClient.id"), index=True, nullable=False
    )
    target_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    # Example event types: 'generation.completed', 'generation.failed'
    event_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    # Hashed secret for signing webhook payloads, allowing verification by the developer
    secret_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship to APIClient
    api_client: Mapped["APIClient"] = relationship("APIClient", back_populates="webhooks")

    def __repr__(self):
        return f"<Webhook(id={self.id}, event_type='{self.event_type}', target_url='{self.target_url}')>"