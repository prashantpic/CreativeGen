"""
SQLAlchemy ORM model for Model Validation Results.

This file defines the database table structure for the 'aimodelvalidationresults'
table, which stores the outcomes of various validation processes for AI model versions.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .ai_model_orm import Base


class AIModelValidationResultORM(Base):
    """
    SQLAlchemy ORM model for the `aimodelvalidationresults` table.

    This class maps to the `aimodelvalidationresults` table in the PostgreSQL
    database. It stores the results of validation scans, including the scan type,
    status, a summary, and a link to detailed report artifacts.
    """
    __tablename__ = "aimodelvalidationresults"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("aimodelversions.id"), nullable=False, index=True)
    scan_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, index=True)
    summary = Column(Text, nullable=True)
    details_path = Column(String(1024), nullable=True)  # Path in MinIO to full report
    validated_at = Column(DateTime, nullable=True)
    validated_by_user_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    model_version = relationship("AIModelVersionORM", back_populates="validation_results")

    def __repr__(self):
        return f"<AIModelValidationResultORM(id={self.id}, version_id={self.model_version_id}, type='{self.scan_type}')>"