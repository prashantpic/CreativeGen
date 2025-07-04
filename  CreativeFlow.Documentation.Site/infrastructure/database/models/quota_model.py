```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QuotaModel(Base):
    """
    SQLAlchemy ORM model for API quotas.
    This model corresponds to the `quotas` table.
    """
    __tablename__ = "quotas"
    
    # id is inherited from Base

    api_client_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("api_keys.id"), unique=True, index=True, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), index=True, nullable=False)
    limit_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., 'daily', 'monthly'
    last_reset_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<QuotaModel(id={self.id}, api_client_id='{self.api_client_id}', limit={self.limit_amount})>"
```