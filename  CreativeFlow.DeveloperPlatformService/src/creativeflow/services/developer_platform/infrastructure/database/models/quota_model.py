from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class QuotaModel(Base):
    """
    SQLAlchemy ORM model for the 'quotas' table.

    This table stores API usage quota configurations for individual API clients.
    It defines the limits and reset periods for billable actions.
    """

    __tablename__ = "quotas"

    api_client_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("api_keys.id"),
        unique=True,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        # ForeignKey("users.id"), # This would be a real FK to a users table
        index=True,
        nullable=False,
    )
    limit_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "monthly", "daily"
    last_reset_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    
    api_key = relationship("APIKeyModel", back_populates="quota")

    def __repr__(self) -> str:
        return f"<QuotaModel(id={self.id}, api_client_id='{self.api_client_id}', limit={self.limit_amount})>"