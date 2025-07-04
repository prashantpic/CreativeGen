"""
SQLAlchemy ORM model for the `aimodelfeedback` table.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from . import Base


class AIModelFeedbackORM(Base):
    """
    SQLAlchemy ORM class for AI Model Feedback.

    Maps to the `aimodelfeedback` table in the PostgreSQL database.
    """
    __tablename__ = "aimodelfeedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("aimodelversions.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    generation_request_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    rating = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    feedback_data = Column(JSONB, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    model_version = relationship("AIModelVersionORM", back_populates="feedbacks")