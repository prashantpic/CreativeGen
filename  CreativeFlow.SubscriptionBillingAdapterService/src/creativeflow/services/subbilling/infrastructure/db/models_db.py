import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# The base class for all our ORM models
Base = declarative_base()

class User(Base):
    """
    SQLAlchemy ORM model representing a read-only projection of the 'users' table
    from the main application database.

    This model provides necessary context for the Subscription & Billing Adapter,
    such as linking the platform's user ID to Odoo's partner ID. It is not
    intended for write operations from this service, as the User Management service
    and Odoo are the sources of truth for this data.
    """
    __tablename__ = "users"

    # The primary key, matching the main application's user ID.
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        index=True,
        doc="The user's unique identifier (UUID) in the CreativeFlow platform."
    )

    # The user's current subscription tier. This is a local projection for quick
    # access. Odoo is the source of truth.
    subscription_tier: Mapped[str] = mapped_column(
        String(50), 
        nullable=False, 
        default='Free',
        doc="The user's current subscription tier (e.g., 'Free', 'Pro'). Synced from Odoo."
    )

    # The user's current credit balance. This is also a local projection.
    # Odoo is the source of truth.
    credit_balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False, 
        default=Decimal("0.00"),
        doc="The user's current credit balance. Synced from Odoo."
    )

    # The crucial link to the corresponding customer record in Odoo.
    odoo_partner_id: Mapped[Optional[int]] = mapped_column(
        Integer, 
        unique=True, 
        index=True, 
        nullable=True,
        doc="The ID of the corresponding 'res.partner' record in Odoo."
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f"odoo_partner_id={self.odoo_partner_id}, "
            f"subscription_tier='{self.subscription_tier}')>"
        )