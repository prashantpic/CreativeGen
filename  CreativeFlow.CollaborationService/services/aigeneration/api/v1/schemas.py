from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from datetime import datetime

# --- Base and Utility Schemas ---

class CustomDimensions(BaseModel):
    """Defines custom width and height for an output."""
    width: int = Field(..., gt=0, description="Width in pixels.")
    height: int = Field(..., gt=0, description="Height in pixels.")

class AssetInfoBase(BaseModel):
    """Base schema for information about a generated asset."""
    asset_id: str = Field(..., description="MinIO path or internal asset ID.")
    url: str = Field(..., description="Publicly accessible or presigned URL for the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png', 'jpg'.")

class SampleAssetInfo(AssetInfoBase):
    """Information specific to a generated sample asset."""
    pass

class FinalAssetInfo(AssetInfoBase):
    """Information specific to a final generated asset."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the final asset.")

# --- API Endpoint Schemas ---

# 4.1.1 Create Generation Request
class GenerationRequestCreate(BaseModel):
    """Schema for creating a new generation request."""
    user_id: str = Field(..., description="The ID of the user initiating the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")
    input_prompt: str = Field(..., min_length=1, max_length=4096, description="The main text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, max_length=2048, description="Additional guidance on the desired style.")
    output_format: str = Field(..., description="The desired output format, e.g., 'InstagramPost_1x1', 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for input images.")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints for the target platform, e.g., 'instagram', 'facebook'.")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

    @validator('custom_dimensions', pre=True, always=True)
    def check_custom_dimensions(cls, v, values):
        if values.get('output_format') == 'Custom' and v is None:
            raise ValueError('custom_dimensions is required when output_format is "Custom"')
        if values.get('output_format') != 'Custom' and v is not None:
            raise ValueError('custom_dimensions should only be provided when output_format is "Custom"')
        return v

# 4.1.2 Get Generation Request Status & General Response
class GenerationRequestRead(BaseModel):
    """Schema for reading generation request details."""
    id: UUID
    user_id: str
    project_id: str
    status: str
    input_prompt: str
    style_guidance: Optional[str]
    output_format: str
    custom_dimensions: Optional[CustomDimensions]
    sample_asset_infos: Optional[List[SampleAssetInfo]] = []
    final_asset_info: Optional[FinalAssetInfo] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 4.1.3 Select Sample for Final Generation
class SampleSelection(BaseModel):
    """Schema for selecting a sample to proceed to final generation."""
    selected_sample_id: str = Field(..., description="The asset_id of the chosen sample.")
    user_id: str = Field(..., description="The ID of the user making the selection.")
    desired_resolution: Optional[str] = Field(None, description="Desired final resolution, e.g., '4096x4096', '4K'.")

# 4.1.4 Regenerate Samples
class RegenerateSamplesRequest(BaseModel):
    """Schema for requesting sample regeneration."""
    user_id: str = Field(..., description="The ID of the user requesting regeneration.")
    updated_prompt: Optional[str] = Field(None, min_length=1, max_length=4096, description="An optional new prompt for regeneration.")
    updated_style_guidance: Optional[str] = Field(None, max_length=2048, description="Optional new style guidance.")

# --- n8n Callback Schemas ---

# 4.2.1 Handle n8n Sample Generation Callback
class N8NSampleResultPayload(BaseModel):
    generation_request_id: UUID
    status: str = Field("AWAITING_SELECTION", const=True)
    samples: List[SampleAssetInfo]

# 4.2.2 Handle n8n Final Generation Callback
class N8NFinalResultPayload(BaseModel):
    generation_request_id: UUID
    status: str = Field("COMPLETED", const=True)
    final_asset: FinalAssetInfo

# 4.2.3 Handle n8n Error Callback
class N8NErrorPayload(BaseModel):
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="e.g., 'sample_processing', 'final_processing'")

# --- Error Response Schemas ---

class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    detail: Union[str, List[ErrorDetail]]