from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any
from uuid import UUID
from datetime import datetime

# --- Base and Common Models ---

class AssetInfoBase(BaseModel):
    """Base model for asset information."""
    asset_id: str = Field(..., description="MinIO path or internal asset ID.")
    url: str = Field(..., description="Publicly accessible URL or presigned URL for the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png'.")

class SampleAssetInfo(AssetInfoBase):
    """Represents a generated sample asset."""
    pass

class FinalAssetInfo(AssetInfoBase):
    """Represents a final generated asset, may have additional metadata."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata about the final asset.")

class CustomDimensions(BaseModel):
    """Model for custom output dimensions."""
    width: int = Field(..., gt=0, description="Width of the custom output in pixels.")
    height: int = Field(..., gt=0, description="Height of the custom output in pixels.")

# --- API Request Models ---

class GenerationRequestBase(BaseModel):
    """Base fields for a generation request."""
    input_prompt: str = Field(..., min_length=1, description="The main text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, description="Additional guidance on the desired style.")
    output_format: str = Field(..., description="Desired output format, e.g., 'InstagramPost_1x1', 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for user-uploaded images.")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints about the target platform, e.g., ['facebook', 'instagram'].")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

class GenerationRequestCreate(GenerationRequestBase):
    """Schema for creating a new generation request."""
    user_id: str = Field(..., description="The ID of the user making the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")
    
    class Config:
        orm_mode = False # Not an ORM model

class SampleSelection(BaseModel):
    """Schema for selecting a sample to generate a final asset from."""
    selected_sample_id: str = Field(..., description="The asset_id of the chosen sample.")
    user_id: str = Field(..., description="The ID of the user making the selection, for authorization.")
    desired_resolution: Optional[str] = Field(None, description="Desired final resolution, e.g., '4096x4096' or '4K'.")

class RegenerateSamplesRequest(BaseModel):
    """Schema for requesting a regeneration of samples."""
    user_id: str = Field(..., description="The ID of the user making the request, for authorization.")
    updated_prompt: Optional[str] = Field(None, description="An optional new or updated prompt for regeneration.")
    updated_style_guidance: Optional[str] = Field(None, description="Optional updated style guidance.")

# --- API Response Models ---

class GenerationRequestRead(GenerationRequestBase):
    """Schema for reading/returning generation request details."""
    id: UUID = Field(..., description="The unique ID of the generation request.")
    user_id: str = Field(..., description="The ID of the user who made the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")
    status: str = Field(..., description="The current status of the generation request.")
    created_at: datetime = Field(..., description="Timestamp of when the request was created.")
    updated_at: datetime = Field(..., description="Timestamp of the last update to the request.")
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="The final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the request failed.")

    class Config:
        orm_mode = True

class ErrorDetail(BaseModel):
    """Schema for a single validation error detail."""
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    """Schema for structured error responses."""
    detail: Union[str, List[ErrorDetail]]


# --- n8n Callback Payloads ---

class N8NSampleResultPayload(BaseModel):
    """Payload received from n8n when sample generation is complete."""
    generation_request_id: UUID
    status: str # Should match a GenerationStatus enum value, e.g., "AWAITING_SELECTION"
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    """Payload received from n8n when final asset generation is complete."""
    generation_request_id: UUID
    status: str # Should match a GenerationStatus enum value, e.g., "COMPLETED"
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    """Payload received from n8n when an error occurs."""
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="Stage where failure occurred, e.g., 'sample_processing', 'final_processing'.")