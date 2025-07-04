from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import UUID as UUIDType
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models in the application.
    It includes a default UUID primary key column.
    """

    id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True), primary_key=True, default=uuid4
    )