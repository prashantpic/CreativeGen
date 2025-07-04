from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UsageRecordModel(Base):
    """
    SQLAlchemy ORM model for the 'api_usage_records' table.

    This table logs individual API calls made by developers for tracking,
    billing, and quota enforcement purposes.
    """

    __tablename__ = "api_usage_records"

    api_client_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("api_keys.id"), index=True
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        # ForeignKey("users.id"), # This would be a real FK to a users table
        index=True,
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    endpoint: Mapped[str] = mapped_column(String(255), index=True)
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=True)
    is_successful: Mapped[bool] = mapped_column(Boolean, default=True)
    
    api_key = relationship("APIKeyModel", back_populates="usage_records")

    def __repr__(self) -> str:
        return f"<UsageRecordModel(id={self.id}, api_client_id='{self.api_client_id}', endpoint='{self.endpoint}')>"