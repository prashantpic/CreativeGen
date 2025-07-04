"""
Pydantic schemas for Model Validation API requests and responses.

These schemas define the data structures for interacting with the `/validation`
API endpoints, used for triggering and monitoring model validation processes.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_config

from creativeflow.mlops_service.domain.enums import ValidationStatusEnum


class ValidationRequestSchema(BaseModel):
    """Schema for requesting a new model validation run."""
    scan_types: List[str] = Field(
        ...,
        description="List of scan types to perform.",
        examples=[["security", "functional", "performance"]]
    )


class ValidationResultBaseSchema(BaseModel):
    """Base schema for validation result attributes."""
    model_version_id: UUID
    scan_type: str = Field(..., max_length=100, description="The type of scan performed.")
    status: ValidationStatusEnum
    summary: Optional[str] = Field(None, max_length=1000, description="A summary of the validation result.")


class ValidationResultResponseSchema(ValidationResultBaseSchema):
    """Schema for API responses containing validation result data."""
    id: UUID
    details_path: Optional[str] = Field(None, description="Path to the full validation report in storage.")
    validated_at: datetime
    validated_by_user_id: Optional[UUID] = None

    @model_config
    class Config:
        from_attributes = True