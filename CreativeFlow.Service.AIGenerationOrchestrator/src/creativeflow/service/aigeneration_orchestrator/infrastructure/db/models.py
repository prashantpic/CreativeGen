"""
Defines the SQLAlchemy ORM model for the GenerationRequest entity, mapping it to
the `generation_requests` table in the PostgreSQL database.
"""

from sqlalchemy import (Column, DateTime, DECIMAL, Enum as EnumDB,
                        JSON, String, Text)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base

from ...domain.models.generation_request import GenerationStatus

Base = declarative_base()


class GenerationRequestORM(Base):
    """
    SQLAlchemy ORM class for the generation_requests table.
    """
    __tablename__ = "generation_requests"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    userId = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    projectId = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    inputPrompt = Column(Text, nullable=False)
    styleGuidance = Column(Text, nullable=True)
    inputParameters = Column(JSON, nullable=False)
    status = Column(EnumDB(GenerationStatus, name="generation_status_enum", create_type=False), nullable=False, index=True)
    errorMessage = Column(Text, nullable=True)
    sampleAssets = Column(JSON, nullable=True)
    selectedSampleId = Column(PG_UUID(as_uuid=True), nullable=True)
    finalAssetId = Column(PG_UUID(as_uuid=True), nullable=True)
    creditsCostSample = Column(DECIMAL(10, 2), nullable=True)
    creditsCostFinal = Column(DECIMAL(10, 2), nullable=True)
    aiModelUsed = Column(String(100), nullable=True)
    createdAt = Column(DateTime(timezone=True), nullable=False)
    updatedAt = Column(DateTime(timezone=True), nullable=False)