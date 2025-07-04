from datetime import datetime
from typing import List, Optional, Union, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl, validator

# --- Base and Common Schemas ---

class CustomDimensions(BaseModel):
    width: int = Field(..., gt=0, description="Width of the custom output in pixels.")
    height: int = Field(..., gt=0, description="Height of the custom output in pixels.")

class AssetInfoBase(BaseModel):
    asset_id: str = Field(..., description="MinIO path or internal asset ID.")
    url: HttpUrl = Field(..., description="Publicly accessible URL or presigned URL for the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png'.")

class SampleAssetInfo(AssetInfoBase):
    pass

class FinalAssetInfo(AssetInfoBase):
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata associated with the final asset.")

class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    detail: Union[str, List[ErrorDetail]]


# --- Generation Request API Schemas ---

class GenerationRequestBase(BaseModel):
    project_id: str = Field(..., description="Identifier for the project this request belongs to.")
    input_prompt: str = Field(..., min_length=1, max_length=4000, description="The main text prompt for generation.")
    style_guidance: Optional[str] = Field(None, max_length=2000, description="Guidance on the desired visual style.")
    output_format: str = Field("InstagramPost_1x1", description="Desired output format, e.g., 'InstagramPost_1x1', 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use for this generation.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of MinIO paths or asset IDs for user-uploaded images.")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints for the target social media platform.")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the output.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

class GenerationRequestCreate(GenerationRequestBase):
    user_id: str = Field(..., description="Identifier for the user initiating the request.")

    @validator('custom_dimensions', pre=True, always=True)
    def check_custom_dimensions(cls, v, values):
        if values.get('output_format') == 'Custom' and v is None:
            raise ValueError('custom_dimensions are required when output_format is "Custom"')
        if values.get('output_format') != 'Custom' and v is not None:
            raise ValueError('custom_dimensions should only be provided when output_format is "Custom"')
        return v

class GenerationRequestRead(GenerationRequestBase):
    id: UUID = Field(..., description="The unique ID of the generation request.")
    user_id: str = Field(..., description="Identifier of the user who initiated the request.")
    status: str = Field(..., description="The current status of the generation request.")
    created_at: datetime
    updated_at: datetime
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="Information about generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="Information about the generated final asset.")
    error_message: Optional[str] = Field(None, description="Error message if the generation failed.")
    credits_cost_sample: Optional[float] = Field(None, description="Credits consumed for sample generation.")
    credits_cost_final: Optional[float] = Field(None, description="Credits consumed for final asset generation.")
    
    class Config:
        orm_mode = True

class SampleSelection(BaseModel):
    selected_sample_id: str = Field(..., description="Asset ID of the chosen sample for final generation.")
    user_id: str = Field(..., description="User ID for authorization and credit check context.")
    desired_resolution: Optional[str] = Field(None, description="e.g., '1024x1024', '4K'. Defaults to a standard HD if not provided.")

class RegenerateSamplesRequest(BaseModel):
    user_id: str = Field(..., description="User ID for authorization and credit check context.")
    updated_prompt: Optional[str] = Field(None, max_length=4000, description="Optional new prompt for regeneration.")
    updated_style_guidance: Optional[str] = Field(None, max_length=2000, description="Optional updated style guidance.")


# --- n8n Callback API Schemas ---

class N8NSampleResultPayload(BaseModel):
    generation_request_id: UUID
    status: str # Should ideally be an enum, e.g., "AWAITING_SELECTION"
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    generation_request_id: UUID
    status: str # Should ideally be an enum, e.g., "COMPLETED"
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="e.g., 'sample_processing', 'final_processing'")