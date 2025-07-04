```python
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IdMixin


class UsageRecordModel(Base, IdMixin):
    __tablename__ = "api_usage_records"

    api_client_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("api_keys.id"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    endpoint: Mapped[str] = mapped_column(String(255))
    is_successful: Mapped[bool] = mapped_column(Boolean)
    cost: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    
    api_key = relationship("APIKeyModel")

    def __repr__(self):
        return f"<UsageRecordModel(id={self.id}, client_id='{self.api_client_id}')>"
```