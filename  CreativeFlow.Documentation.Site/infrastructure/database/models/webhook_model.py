```python
import uuid
from datetime import datetime

from sqlalchemy import ARRAY, Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class WebhookModel(Base):
    """
    SQLAlchemy ORM model for webhooks.
    This model corresponds to the `webhooks` table.
    """
    __tablename__ = "webhooks"

    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), index=True, nullable=False)
    target_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    event_types: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    hashed_secret: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<WebhookModel(id={self.id}, user_id='{self.user_id}', url='{self.target_url[:30]}...')>"
```