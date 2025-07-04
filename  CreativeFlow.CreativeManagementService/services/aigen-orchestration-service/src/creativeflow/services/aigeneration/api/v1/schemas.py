"""
Pydantic Schemas for API Data Contracts.

This module defines all Pydantic models used for API request and response
bodies, as well as for n8n callback payloads. These models ensure data
validation, serialization, and clear API documentation.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator

# --- Base and Common Models ---

class CustomDimensions(BaseModel):
    """Defines custom width and height for an output format."""
    width: int = Field(..., gt=0, description="Width in pixels.")
    height: int = Field(..., gt=0, description="Height in pixels.")

class AssetInfoBase(BaseModel):
    """Base model for asset information."""
    asset_id: str = Field(..., description="MinIO path or internal asset ID.")
    url: str = Field(..., description="Publicly accessible URL or presigned URL for the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png'.")

class SampleAssetInfo(AssetInfoBase):
    """Represents a single generated sample asset."""
    pass

class FinalAssetInfo(AssetInfoBase):
    """Represents the final generated asset."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the final asset.")

# --- Generation Request API Schemas ---

class GenerationRequestBase(BaseModel):
    """Base fields for a generation request."""
    input_prompt: str = Field(..., min_length=1, description="The main text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, description="Additional guidance on the desired style.")
    output_format: str = Field(..., description="The desired output format, e.g., 'InstagramPost_1x1', 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use for this generation.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for user-uploaded images.")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints about the target social media platform.")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

    @validator('custom_dimensions', pre=True, always=True)
    def check_custom_dimensions(cls, v, values):
        if values.get('output_format') == 'Custom' and v is None:
            raise ValueError('custom_dimensions is required when output_format is "Custom"')
        if values.get('output_format') != 'Custom' and v is not None:
            raise ValueError('custom_dimensions should only be provided when output_format is "Custom"')
        return v

class GenerationRequestCreate(GenerationRequestBase):
    """Schema for creating a new generation request."""
    user_id: str = Field(..., description="The ID of the user initiating the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")

class GenerationRequestRead(GenerationRequestBase):
    """Schema for reading a generation request's details from the API."""
    id: UUID = Field(..., description="The unique ID of the generation request.")
    user_id: str = Field(..., description="The ID of the user who initiated the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")
    status: str = Field(..., description="The current status of the generation request.")
    created_at: datetime = Field(..., description="Timestamp when the request was created.")
    updated_at: datetime = Field(..., description="Timestamp when the request was last updated.")
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="The final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the generation failed.")

    class Config:
        orm_mode = True

class SampleSelection(BaseModel):
    """Schema for selecting a sample to generate the final asset."""
    selected_sample_id: str = Field(..., description="Asset ID of the chosen sample.")
    user_id: str = Field(..., description="ID of the user making the selection for authorization context.")
    desired_resolution: Optional[str] = Field(None, description="Desired resolution for the final asset, e.g., '4096x4096'.")

class RegenerateSamplesRequest(BaseModel):
    """Schema for triggering a regeneration of samples."""
    user_id: str = Field(..., description="ID of the user requesting regeneration for authorization context.")
    updated_prompt: Optional[str] = Field(None, description="Optional new prompt for the regeneration.")
    updated_style_guidance: Optional[str] = Field(None, description="Optional new style guidance for regeneration.")

# --- n8n Callback API Schemas ---

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
    failed_stage: Optional[str] = Field(None, description="Stage where failure occurred, e.g., 'sample_processing', 'final_processing'.")


# --- Error Response Schemas ---

class ErrorDetail(BaseModel):
    """Detailed information for a validation error."""
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    """Standardized error response body."""
    detail: Union[str, List[ErrorDetail]]