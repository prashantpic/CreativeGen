from datetime import datetime
from typing import List, Optional, Union, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, validator

# --- Base and Shared Models ---

class AssetInfoBase(BaseModel):
    """Base model for asset information."""
    asset_id: str = Field(..., description="Unique identifier for the asset, e.g., a MinIO path or internal ID.")
    url: str = Field(..., description="URL to access the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png', 'jpg'.")

    class Config:
        orm_mode = True

class SampleAssetInfo(AssetInfoBase):
    """Asset information specific to generated samples."""
    pass

class FinalAssetInfo(AssetInfoBase):
    """Asset information specific to the final generated asset."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the final asset.")

class CustomDimensions(BaseModel):
    """Custom dimensions for output format."""
    width: int = Field(..., gt=0, description="Width of the custom output in pixels.")
    height: int = Field(..., gt=0, description="Height of the custom output in pixels.")


# --- Generation Request API Schemas ---

class GenerationRequestBase(BaseModel):
    """Base model with common fields for a generation request."""
    input_prompt: str = Field(..., min_length=1, max_length=4000, description="The main text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, max_length=2000, description="Additional guidance on the desired style.")
    output_format: str = Field(..., description="Desired output format, e.g., 'InstagramPost_1x1', 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of references to user-uploaded images (e.g., MinIO paths).")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints for the target platform, e.g., ['instagram', 'facebook'].")
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
    """Schema for reading generation request data from the API."""
    id: UUID = Field(..., description="The unique identifier for the generation request.")
    status: str = Field(..., description="The current status of the generation request.")
    user_id: str = Field(..., description="The ID of the user who initiated the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")
    created_at: datetime = Field(..., description="Timestamp of when the request was created.")
    updated_at: datetime = Field(..., description="Timestamp of the last update to the request.")
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="Information about the generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="Information about the final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the generation failed.")

    class Config:
        orm_mode = True

class SampleSelection(BaseModel):
    """Schema for selecting a sample to proceed with final generation."""
    selected_sample_id: str = Field(..., description="The asset_id of the chosen sample.")
    user_id: str = Field(..., description="The ID of the user making the selection (for context).")
    desired_resolution: Optional[str] = Field(None, description="Desired resolution for the final asset, e.g., '1024x1024', '4K'.")

class RegenerateSamplesRequest(BaseModel):
    """Schema for requesting sample regeneration."""
    user_id: str = Field(..., description="The ID of the user requesting regeneration (for context).")
    updated_prompt: Optional[str] = Field(None, min_length=1, max_length=4000, description="Optional new prompt for regeneration.")
    updated_style_guidance: Optional[str] = Field(None, max_length=2000, description="Optional new style guidance.")


# --- n8n Callback Schemas ---

class N8NSampleResultPayload(BaseModel):
    """Payload received from n8n when sample generation is complete."""
    generation_request_id: UUID
    status: str # Expected to be "AWAITING_SELECTION"
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    """Payload received from n8n when final asset generation is complete."""
    generation_request_id: UUID
    status: str # Expected to be "COMPLETED"
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    """Payload received from n8n when an error occurs during processing."""
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="The stage where failure occurred, e.g., 'sample_processing', 'final_processing'.")


# --- Error Response Schemas ---

class ErrorDetail(BaseModel):
    """Schema for a single validation error detail."""
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    """Schema for a generic error response."""
    detail: Union[str, List[ErrorDetail]]