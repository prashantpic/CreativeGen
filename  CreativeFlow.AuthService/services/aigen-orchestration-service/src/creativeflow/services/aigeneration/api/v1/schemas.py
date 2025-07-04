from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from pydantic import BaseModel, Field

# --- Base and Utility Schemas ---

class AssetInfoBase(BaseModel):
    """Base schema for asset information."""
    asset_id: str = Field(..., description="MinIO path or internal asset ID")
    url: str = Field(..., description="Publicly accessible URL or presigned URL for the asset")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'")
    format: str = Field(..., description="File format of the asset, e.g., 'png', 'jpg'")

    class Config:
        orm_mode = True

class SampleAssetInfo(AssetInfoBase):
    """Schema for a generated sample asset."""
    pass

class FinalAssetInfo(AssetInfoBase):
    """Schema for a final generated asset."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the final asset")

class CustomDimensions(BaseModel):
    """Schema for custom output dimensions."""
    width: int = Field(..., gt=0, description="Width of the creative in pixels")
    height: int = Field(..., gt=0, description="Height of the creative in pixels")

# --- API Request Schemas ---

class GenerationRequestBase(BaseModel):
    """Base schema with common fields for a generation request."""
    input_prompt: str = Field(..., description="The main text prompt for the AI generation")
    style_guidance: Optional[str] = Field(None, description="Keywords or description of the desired style")
    output_format: str = Field(..., description="Predefined output format, e.g., 'InstagramPost_1x1', or 'Custom'")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use for brand elements")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for user-uploaded images")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints about the target social media platform")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation")

class GenerationRequestCreate(GenerationRequestBase):
    """Schema for creating a new generation request."""
    user_id: str = Field(..., description="The ID of the user initiating the request")
    project_id: str = Field(..., description="The ID of the project this request belongs to")

class SampleSelection(BaseModel):
    """Schema for selecting a sample for final generation."""
    selected_sample_id: str = Field(..., description="The asset_id of the chosen sample creative")
    user_id: str = Field(..., description="The ID of the user making the selection for authorization")
    desired_resolution: Optional[str] = Field(None, description="Desired final resolution, e.g., '4096x4096' or '4K'")

class RegenerateSamplesRequest(BaseModel):
    """Schema for triggering a sample regeneration."""
    user_id: str = Field(..., description="The ID of the user making the request for authorization")
    updated_prompt: Optional[str] = Field(None, description="An optional new or refined prompt for the regeneration")
    updated_style_guidance: Optional[str] = Field(None, description="Optional new or refined style guidance")

# --- API Response Schemas ---

class GenerationRequestRead(GenerationRequestBase):
    """Schema for reading/responding with generation request details."""
    id: UUID = Field(..., description="The unique identifier for the generation request")
    user_id: str = Field(..., description="The ID of the user who initiated the request")
    project_id: str = Field(..., description="The ID of the project this request belongs to")
    status: str = Field(..., description="The current status of the generation request")
    created_at: datetime = Field(..., description="Timestamp of when the request was created")
    updated_at: datetime = Field(..., description="Timestamp of the last update to the request")
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="The final generated asset")
    error_message: Optional[str] = Field(None, description="Error message if the request failed")

    class Config:
        orm_mode = True

class ErrorDetail(BaseModel):
    """Schema for a single validation error."""
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    """Schema for a structured error response."""
    detail: Union[str, List[ErrorDetail]]

# --- n8n Callback Schemas ---

class N8NSampleResultPayload(BaseModel):
    """Schema for the callback from n8n after sample generation."""
    generation_request_id: UUID
    status: str # Should be "AWAITING_SELECTION"
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    """Schema for the callback from n8n after final asset generation."""
    generation_request_id: UUID
    status: str # Should be "COMPLETED"
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    """Schema for the callback from n8n when an error occurs."""
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="Stage where failure occurred, e.g., 'sample_processing'")