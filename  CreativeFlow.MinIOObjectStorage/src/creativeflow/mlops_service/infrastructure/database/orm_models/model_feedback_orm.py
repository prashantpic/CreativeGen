"""
SQLAlchemy ORM model for Model Feedback.

This file defines the database table structure for the 'aimodelfeedback' table,
which stores user-provided feedback on AI models and their outputs.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .ai_model_orm import Base


class AIModelFeedbackORM(Base):
    """
    SQLAlchemy ORM model for the `aimodelfeedback` table.

    This class maps to the `aimodelfeedback` table in the PostgreSQL database.
    It stores user feedback, including ratings and comments, and links it to
    the relevant model version, user, and generation request.
    """
    __tablename__ = "aimodelfeedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("aimodelversions.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    generation_request_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    rating = Column(Integer, nullable=True)  # e.g., 1-5
    comment = Column(Text, nullable=True)
    feedback_data = Column(JSONB, nullable=True)  # For structured feedback
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    model_version = relationship("AIModelVersionORM", back_populates="feedbacks")

    def __repr__(self):
        return f"<AIModelFeedbackORM(id={self.id}, version_id={self.model_version_id}, user_id={self.user_id})>"