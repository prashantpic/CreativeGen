"""
Pydantic model for storing the results of model validation and security scans.

This class captures the outcome of various checks performed on a model version
before it can be approved for deployment.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from creativeflow.mlops_service.domain.enums import ValidationStatusEnum


class ValidationResult(BaseModel):
    """
    Represents the outcome of a validation process for an AI model version.

    Attributes:
        id: The unique identifier for this validation run.
        model_version_id: The ID of the AIModelVersion that was validated.
        scan_type: The type of scan performed (e.g., 'security_container').
        status: The outcome status of the validation (e.g., 'PASSED', 'FAILED').
        summary: A brief summary of the validation result.
        details_path: A path in object storage to the full detailed report.
        validated_at: The timestamp when the validation was completed.
        validated_by_user_id: The user/system that initiated the validation.
    """
    id: UUID
    model_version_id: UUID
    scan_type: str = Field(..., max_length=100)
    status: ValidationStatusEnum
    summary: Optional[str] = Field(None, max_length=1000)
    details_path: Optional[str] = None
    validated_at: datetime
    validated_by_user_id: Optional[UUID] = None