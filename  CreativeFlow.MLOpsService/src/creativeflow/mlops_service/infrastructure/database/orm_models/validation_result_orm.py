"""
SQLAlchemy ORM model for the `aimodelvalidationresults` table.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import Base


class AIModelValidationResultORM(Base):
    """
    SQLAlchemy ORM class for AI Model Validation Results.

    Maps to the `aimodelvalidationresults` table in the PostgreSQL database.
    """
    __tablename__ = "aimodelvalidationresults"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("aimodelversions.id"), nullable=False, index=True)
    scan_type = Column(String(100), nullable=False)
    status = Column(String(50), index=True, nullable=False)
    summary = Column(Text, nullable=True)
    details_path = Column(String, nullable=True) # Path to full report in MinIO
    validated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    validated_by_user_id = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    model_version = relationship("AIModelVersionORM", back_populates="validation_results")