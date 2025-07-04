"""
This module defines base Pydantic models and configurations to be inherited by all
other Data Transfer Objects (DTOs) in the application. This promotes consistency
and reduces code duplication.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    Base DTO with common configuration.

    - `from_attributes=True`: Allows creating models from ORM objects (e.g., SQLAlchemy models).
    - `populate_by_name=True`: Allows populating model fields by their alias name.
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class BaseResponseDTO(BaseDTO):
    """
    Base DTO for API responses, including common primary key and timestamp fields
    that are present in most database entities.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime