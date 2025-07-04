from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from uuid import UUID

# --- Base and Helper Schemas ---

class CustomDimensions(BaseModel):
    width: int = Field(..., gt=0, description="Width of the custom output in pixels.")
    height: int = Field(..., gt=0, description="Height of the custom output in pixels.")

class AssetInfoBase(BaseModel):
    asset_id: str = Field(..., description="Unique identifier for the asset (e.g., MinIO path or internal ID).")
    url: str = Field(..., description="URL to access the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png', 'jpg'.")

class SampleAssetInfo(AssetInfoBase):
    pass

class FinalAssetInfo(AssetInfoBase):
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the final asset.")

# --- API Endpoint Schemas: Generation Requests ---

class GenerationRequestBase(BaseModel):
    input_prompt: str = Field(..., min_length=1, description="The main text prompt for the AI.")
    style_guidance: Optional[str] = Field(None, description="Guidance on the desired artistic style.")
    output_format: str = Field(..., description="Desired output format, e.g., 'InstagramPost_1x1', 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use for this generation.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of references to user-uploaded images (e.g., MinIO paths).")
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
    user_id: str = Field(..., description="The ID of the user making the request.")
    project_id: str = Field(..., description="The ID of the project this generation belongs to.")

class GenerationRequestRead(GenerationRequestBase):
    id: UUID = Field(..., description="Unique identifier for the generation request.")
    user_id: str = Field(..., description="The ID of the user who made the request.")
    project_id: str = Field(..., description="The ID of the project this generation belongs to.")
    status: str = Field(..., description="Current status of the generation request.")
    created_at: datetime = Field(..., description="Timestamp when the request was created.")
    updated_at: datetime = Field(..., description="Timestamp when the request was last updated.")
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="Information about the final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the generation failed.")
    
    class Config:
        orm_mode = True

class SampleSelection(BaseModel):
    selected_sample_id: str = Field(..., description="The asset ID of the chosen sample for final generation.")
    user_id: str = Field(..., description="ID of the user making the selection (for authorization).")
    desired_resolution: Optional[str] = Field(None, description="Optional desired resolution for the final asset, e.g., '4096x4096', '4K'.")

class RegenerateSamplesRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user making the request (for authorization).")
    updated_prompt: Optional[str] = Field(None, description="An optional new or refined prompt for regeneration.")
    updated_style_guidance: Optional[str] = Field(None, description="Optional new style guidance.")

# --- API Endpoint Schemas: n8n Callbacks ---

class N8NSampleResultPayload(BaseModel):
    generation_request_id: UUID
    status: str # Should be "AWAITING_SELECTION"
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    generation_request_id: UUID
    status: str # Should be "COMPLETED"
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    generation_request_id: UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="Stage where the error occurred, e.g., 'sample_processing', 'final_processing'.")


# --- API Schemas: Error Responses ---
class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    detail: Union[str, List[ErrorDetail]]