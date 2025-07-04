```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass

class IdMixin:
    """A mixin to add a UUID primary key column."""
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
```