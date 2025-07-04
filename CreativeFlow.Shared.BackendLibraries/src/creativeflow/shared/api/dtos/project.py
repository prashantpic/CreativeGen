"""
This module contains Pydantic DTOs for managing the creative workflow,
including Brand Kits, Projects, and related entities. These models serve as the
data contracts for the Creative Management Service's API.
"""
from typing import Any, Dict, List, Optional
from uuid import UUID

from .base import BaseDTO, BaseResponseDTO


# =============================================================================
# Brand Kit DTOs
# =============================================================================

class BrandKitCreateDTO(BaseDTO):
    """DTO for creating a new Brand Kit."""
    name: str
    colors: List[Dict[str, str]]  # e.g., [{"name": "Primary", "hex": "#FF0000"}]
    fonts: List[Dict[str, str]]   # e.g., [{"name": "Heading", "family": "Arial"}]
    logos: Optional[List[Dict[str, str]]] = None  # e.g., [{"name": "Main", "path": "s3_path"}]
    style_preferences: Optional[Dict[str, Any]] = None
    team_id: Optional[UUID] = None  # Optional team association on creation


class BrandKitUpdateDTO(BaseDTO):
    """DTO for updating an existing Brand Kit. All fields are optional."""
    name: Optional[str] = None
    colors: Optional[List[Dict[str, str]]] = None
    fonts: Optional[List[Dict[str, str]]] = None
    logos: Optional[List[Dict[str, str]]] = None
    style_preferences: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None


class BrandKitResponseDTO(BaseResponseDTO, BrandKitCreateDTO):
    """DTO for returning a full Brand Kit resource."""
    is_default: bool
    user_id: UUID


# =============================================================================
# Project DTOs
# =============================================================================

class ProjectCreateDTO(BaseDTO):
    """DTO for creating a new Project."""
    workbench_id: UUID
    name: str
    template_id: Optional[UUID] = None
    brand_kit_id: Optional[UUID] = None
    target_platform: Optional[str] = None


class ProjectUpdateDTO(BaseDTO):
    """DTO for updating an existing Project. All fields are optional."""
    name: Optional[str] = None
    brand_kit_id: Optional[UUID] = None
    target_platform: Optional[str] = None
    collaboration_state: Optional[Dict[str, Any]] = None


class ProjectResponseDTO(BaseResponseDTO, ProjectCreateDTO):
    """DTO for returning a full Project resource."""
    user_id: UUID  # Denormalized for convenience
    last_collaborated_at: Optional[Any] = None