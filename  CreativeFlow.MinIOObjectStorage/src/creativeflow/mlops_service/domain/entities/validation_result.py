"""
Pydantic model for storing the results of model validation and security scans.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from creativeflow.mlops_service.domain.enums import (
    ValidationStatusEnum,
    ValidationScanTypeEnum,
)


class ValidationResult(BaseModel):
    """
    Represents the outcome of a validation process for an AI model version.

    This Pydantic model contains the results of a specific validation run,
    such as a security scan or functional test, including its status and a
    link to a detailed report.
    """
    id: UUID = Field(default_factory=uuid4)
    model_version_id: UUID = Field(..., description="The UUID of the AIModelVersion that was validated.")
    scan_type: ValidationScanTypeEnum = Field(..., description="The type of validation scan performed.")
    status: ValidationStatusEnum = Field(default=ValidationStatusEnum.PENDING, description="The status of the validation process.")
    summary: Optional[str] = Field(None, max_length=1000, description="A summary of the validation findings.")
    details_path: Optional[str] = Field(None, description="The path to the full validation report artifact in object storage (e.g., MinIO).")
    validated_at: Optional[datetime] = Field(None, description="The timestamp when the validation process completed.")
    validated_by_user_id: Optional[UUID] = Field(None, description="The UUID of the user or system that initiated the validation.")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        json_encoders = {
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat() if v else None
        }