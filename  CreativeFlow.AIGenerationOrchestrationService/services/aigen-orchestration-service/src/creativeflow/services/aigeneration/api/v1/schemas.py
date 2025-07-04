"""
schemas.py

Pydantic models for API request and response data structures (DTOs).

This module defines the data contracts for all API endpoints, ensuring
robust validation and clear, self-documenting API specifications.
"""

from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, conint

# --- Base and Common Schemas ---

class CustomDimensions(BaseModel):
    """Defines custom width and height for an output format."""
    width: conint(gt=0, le=8192) = Field(..., description="Width of the creative in pixels.")
    height: conint(gt=0, le=8192) = Field(..., description="Height of the creative in pixels.")

class AssetInfoBase(BaseModel):
    """Base model for asset information."""
    asset_id: str = Field(..., description="Unique identifier for the asset (e.g., MinIO path or internal ID).")
    url: str = Field(..., description="Publicly accessible URL for the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png', 'jpg'.")

class SampleAssetInfo(AssetInfoBase):
    """Information about a generated sample asset."""
    pass

class FinalAssetInfo(AssetInfoBase):
    """Information about a final generated asset."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata associated with the final asset.")

# --- Generation Request Schemas ---

class GenerationRequestCreate(BaseModel):
    """Schema for creating a new generation request."""
    user_id: str = Field(..., description="Identifier of the user requesting the generation.")
    project_id: str = Field(..., description="Identifier of the project this request belongs to.")
    input_prompt: str = Field(..., min_length=1, max_length=4096, description="The main text prompt for the AI.")
    style_guidance: Optional[str] = Field(None, max_length=2048, description="Additional guidance on the desired style.")
    output_format: str = Field(..., description="Desired output format, e.g., 'InstagramPost_1x1', 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="Identifier of the brand kit to use.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for input images.")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints about the target social media platform.")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

class GenerationRequestRead(BaseModel):
    """Schema for reading a generation request's state and results."""
    id: UUID = Field(..., description="The unique identifier of the generation request.")
    user_id: str = Field(..., description="Identifier of the user who requested the generation.")
    project_id: str = Field(..., description="Identifier of the project this request belongs to.")
    status: str = Field(..., description="Current status of the generation request.")
    input_prompt: str = Field(..., description="The original input prompt.")
    created_at: datetime = Field(..., description="Timestamp of when the request was created.")
    updated_at: datetime = Field(..., description="Timestamp of the last update to the request.")
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="The final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the request failed.")
    
    class Config:
        from_attributes = True

# --- API Interaction Schemas ---

class SampleSelection(BaseModel):
    """Schema for selecting a sample to generate a final asset from."""
    selected_sample_id: str = Field(..., description="The asset_id of the chosen sample.")
    user_id: str = Field(..., description="The user ID for authorization and credit check context.")
    desired_resolution: Optional[str] = Field(None, description="Desired final resolution, e.g., '4096x4096', '4K'.")

class RegenerateSamplesRequest(BaseModel):
    """Schema for requesting a regeneration of samples."""
    user_id: str = Field(..., description="The user ID for authorization and credit check context.")
    updated_prompt: Optional[str] = Field(None, max_length=4096, description="Optional new prompt for regeneration.")
    updated_style_guidance: Optional[str] = Field(None, max_length=2048, description="Optional updated style guidance.")

# --- n8n Callback Schemas ---

class N8NSampleResultPayload(BaseModel):
    """Payload received from n8n when sample generation is complete."""
    generation_request_id: UUID
    status: str # e.g., "AWAITING_SELECTION"
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    """Payload received from n8n when final asset generation is complete."""
    generation_request_id: UUID
    status: str # e.g., "COMPLETED"
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    """Payload received from n8n when an error occurs during generation."""
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="Stage where failure occurred, e.g., 'sample_processing'.")

# --- Error Response Schemas ---

class ErrorDetail(BaseModel):
    """Schema for a single validation error detail."""
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    """Schema for a generic error response."""
    detail: Union[str, List[ErrorDetail]]