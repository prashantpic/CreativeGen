from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union, Dict, Any
from uuid import UUID

from ...domain.models.generation_status import GenerationStatus

# --- Base and Common Schemas ---

class CustomDimensions(BaseModel):
    width: int = Field(..., gt=0, description="Width in pixels.")
    height: int = Field(..., gt=0, description="Height in pixels.")

class AssetInfoBase(BaseModel):
    asset_id: str = Field(..., description="MinIO path or internal asset ID.")
    url: str = Field(..., description="Publicly accessible URL or presigned URL for the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png', 'jpg'.")

    class Config:
        orm_mode = True

class SampleAssetInfo(AssetInfoBase):
    pass

class FinalAssetInfo(AssetInfoBase):
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the final asset.")


# --- Generation Request API Schemas ---

class GenerationRequestBase(BaseModel):
    input_prompt: str = Field(..., description="The main text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, description="Additional guidance on the desired style.")
    output_format: str = Field("InstagramPost_1x1", description="Predefined or custom output format.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for input images.")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints for the target platform, e.g., 'Instagram', 'TikTok'.")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

    @validator('custom_dimensions', pre=True, always=True)
    def check_custom_dimensions(cls, v, values):
        if values.get('output_format') == 'Custom' and v is None:
            raise ValueError('custom_dimensions are required when output_format is "Custom"')
        if values.get('output_format') != 'Custom' and v is not None:
            raise ValueError('custom_dimensions should only be provided when output_format is "Custom"')
        return v

class GenerationRequestCreate(GenerationRequestBase):
    user_id: str = Field(..., description="The ID of the user making the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")

class GenerationRequestRead(GenerationRequestBase):
    id: UUID = Field(..., description="The unique identifier of the generation request.")
    user_id: str = Field(..., description="The ID of the user who made the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")
    status: Union[GenerationStatus, str] = Field(..., description="The current status of the generation request.")
    created_at: datetime
    updated_at: datetime
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="The final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the request failed.")
    credits_cost_sample: Optional[float] = Field(None, description="Credits cost for the sample generation phase.")
    credits_cost_final: Optional[float] = Field(None, description="Credits cost for the final generation phase.")

    class Config:
        orm_mode = True
        use_enum_values = True

class SampleSelection(BaseModel):
    selected_sample_id: str = Field(..., description="Asset ID of the chosen sample.")
    user_id: str = Field(..., description="User ID for authorization and credit check context.")
    desired_resolution: Optional[str] = Field(None, description="Desired resolution for the final asset, e.g., '4K'.")

class RegenerateSamplesRequest(BaseModel):
    user_id: str = Field(..., description="User ID for authorization and credit check context.")
    updated_prompt: Optional[str] = Field(None, description="Optional new prompt for regeneration.")
    updated_style_guidance: Optional[str] = Field(None, description="Optional new style guidance.")


# --- n8n Callback Schemas ---

class N8NSampleResultPayload(BaseModel):
    generation_request_id: UUID
    status: str # Should correspond to a GenerationStatus value, e.g., "AWAITING_SELECTION"
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    generation_request_id: UUID
    status: str # Should correspond to a GenerationStatus value, e.g., "COMPLETED"
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    generation_request_id: UUID
    error_code: Optional[str]
    error_message: str
    error_details: Optional[Dict[str, Any]]
    failed_stage: Optional[str] = Field(None, description="Stage where failure occurred, e.g., 'sample_processing'.")


# --- Error Response Schemas ---

class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    detail: Union[str, List[ErrorDetail]]