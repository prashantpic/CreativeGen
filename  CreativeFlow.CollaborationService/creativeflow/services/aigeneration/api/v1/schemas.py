from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator

from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus


# --- Base and Reusable Schemas ---

class AssetInfoBase(BaseModel):
    """Base schema for asset information."""
    asset_id: str = Field(..., description="Identifier for the asset in the asset management system/MinIO")
    url: str = Field(..., description="URL to access the asset")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'")
    format: str = Field(..., description="File format of the asset, e.g., 'png'")

    class Config:
        orm_mode = True


class SampleAssetInfo(AssetInfoBase):
    """Schema for a generated sample asset."""
    pass


class FinalAssetInfo(AssetInfoBase):
    """Schema for a final generated asset, may include extra metadata."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata about the final asset.")


class CustomDimensions(BaseModel):
    """Schema for custom output dimensions."""
    width: int = Field(..., gt=0, description="Width of the custom output in pixels.")
    height: int = Field(..., gt=0, description="Height of the custom output in pixels.")


class GenerationRequestBase(BaseModel):
    """Base schema containing common fields for a generation request."""
    input_prompt: str = Field(..., min_length=1, description="The primary text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, description="Text guidance on the desired style.")
    output_format: str = Field("InstagramPost_1x1", description="Predefined output format or 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for input images.")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints for the target platform, e.g., ['facebook', 'instagram'].")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

    @validator('custom_dimensions', pre=True, always=True)
    def check_custom_dimensions(cls, v, values):
        if values.get('output_format') == 'Custom' and v is None:
            raise ValueError('custom_dimensions are required when output_format is "Custom"')
        if values.get('output_format') != 'Custom' and v is not None:
            raise ValueError('custom_dimensions should only be provided when output_format is "Custom"')
        return v


# --- API Endpoint Schemas ---

class GenerationRequestCreate(GenerationRequestBase):
    """Schema for creating a new generation request."""
    user_id: str = Field(..., description="The ID of the user initiating the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")


class GenerationRequestRead(GenerationRequestBase):
    """Schema for reading/responding with generation request details."""
    id: UUID = Field(..., description="The unique ID of the generation request.")
    status: GenerationStatus = Field(..., description="The current status of the generation request.")
    user_id: str = Field(..., description="The ID of the user who initiated the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")
    created_at: datetime = Field(..., description="Timestamp of when the request was created.")
    updated_at: datetime = Field(..., description="Timestamp of the last update to the request.")
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="The final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the generation failed.")

    class Config:
        orm_mode = True


class SampleSelection(BaseModel):
    """Schema for selecting a sample to proceed with final generation."""
    selected_sample_id: str = Field(..., description="The asset_id of the chosen sample.")
    user_id: str = Field(..., description="The ID of the user making the selection for context/authorization.")
    desired_resolution: Optional[str] = Field(None, description="Desired resolution for the final asset, e.g., '4K'.")


class RegenerateSamplesRequest(BaseModel):
    """Schema for requesting a regeneration of samples."""
    user_id: str = Field(..., description="The ID of the user requesting regeneration for context/authorization.")
    updated_prompt: Optional[str] = Field(None, description="An optional new prompt to guide the regeneration.")
    updated_style_guidance: Optional[str] = Field(None, description="Optional new style guidance.")


# --- n8n Callback Schemas ---

class N8NSampleResultPayload(BaseModel):
    """Schema for the callback from n8n when sample generation is complete."""
    generation_request_id: UUID
    status: str = Field("AWAITING_SELECTION", const=True)
    samples: List[SampleAssetInfo]


class N8NFinalResultPayload(BaseModel):
    """Schema for the callback from n8n when final asset generation is complete."""
    generation_request_id: UUID
    status: str = Field("COMPLETED", const=True)
    final_asset: FinalAssetInfo


class N8NErrorPayload(BaseModel):
    """Schema for the callback from n8n when an error occurs."""
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="e.g., 'sample_processing', 'final_processing'")


# --- Error Response Schemas ---

class ErrorDetail(BaseModel):
    """Schema for a single validation error detail."""
    loc: List[str]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    """Schema for a generic error response."""
    detail: Union[str, List[ErrorDetail]]