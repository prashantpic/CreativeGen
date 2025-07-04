```python
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
import uuid
from pydantic import BaseModel, Field, validator
from creativeflow.services.aigeneration.domain.models.generation_status import GenerationStatus

# --- Base and Common Schemas ---

class CustomDimensions(BaseModel):
    width: int = Field(..., gt=0, description="Width in pixels.")
    height: int = Field(..., gt=0, description="Height in pixels.")

class AssetInfoBase(BaseModel):
    asset_id: str = Field(..., description="Unique identifier for the asset (e.g., MinIO path or internal ID).")
    url: str = Field(..., description="Publicly accessible URL for the asset.")
    resolution: str = Field(..., description="Resolution of the asset, e.g., '1024x1024'.")
    format: str = Field(..., description="File format of the asset, e.g., 'png'.")

class SampleAssetInfo(AssetInfoBase):
    pass

class FinalAssetInfo(AssetInfoBase):
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the final asset.")

# --- API Request Payloads ---

class GenerationRequestBase(BaseModel):
    input_prompt: str = Field(..., min_length=1, description="The main text prompt for the AI generation.")
    style_guidance: Optional[str] = Field(None, description="Additional guidance on the desired style.")
    output_format: str = Field("InstagramPost_1x1", description="Predefined output format or 'Custom'.")
    custom_dimensions: Optional[CustomDimensions] = Field(None, description="Required if output_format is 'Custom'.")
    brand_kit_id: Optional[str] = Field(None, description="ID of the brand kit to use.")
    uploaded_image_references: Optional[List[str]] = Field(None, description="List of references to uploaded images (e.g., MinIO paths).")
    target_platform_hints: Optional[List[str]] = Field(None, description="Hints for the target platform, e.g., ['facebook', 'story'].")
    emotional_tone: Optional[str] = Field(None, description="Desired emotional tone of the creative.")
    cultural_adaptation_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for cultural adaptation.")

    @validator('custom_dimensions', always=True)
    def check_custom_dimensions(cls, v, values):
        if values.get('output_format') == 'Custom' and v is None:
            raise ValueError('custom_dimensions is required when output_format is "Custom"')
        return v

class GenerationRequestCreate(GenerationRequestBase):
    user_id: str = Field(..., description="The ID of the user initiating the request.")
    project_id: str = Field(..., description="The ID of the project this request belongs to.")

class SampleSelection(BaseModel):
    selected_sample_id: str = Field(..., description="The asset_id of the chosen sample for final generation.")
    user_id: str = Field(..., description="The ID of the user making the selection.")
    desired_resolution: Optional[str] = Field(None, description="Desired resolution for the final asset, e.g., '4096x4096' or '4K'.")

class RegenerateSamplesRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user requesting regeneration.")
    updated_prompt: Optional[str] = Field(None, description="An optional new prompt to guide the regeneration.")
    updated_style_guidance: Optional[str] = Field(None, description="Optional new style guidance.")


# --- API Response Payloads ---

class GenerationRequestRead(GenerationRequestBase):
    id: uuid.UUID = Field(..., description="The unique identifier for the generation request.")
    status: GenerationStatus = Field(..., description="The current status of the generation request.")
    created_at: datetime
    updated_at: datetime
    sample_asset_infos: Optional[List[SampleAssetInfo]] = Field(None, description="List of generated sample assets.")
    final_asset_info: Optional[FinalAssetInfo] = Field(None, description="The final generated asset.")
    error_message: Optional[str] = Field(None, description="Error message if the request failed.")

    class Config:
        orm_mode = True

# --- n8n Callback Payloads ---

class N8NSampleResultPayload(BaseModel):
    generation_request_id: uuid.UUID
    status: str = Field(..., description="Should be 'AWAITING_SELECTION' or similar.")
    samples: List[SampleAssetInfo]

class N8NFinalResultPayload(BaseModel):
    generation_request_id: uuid.UUID
    status: str = Field(..., description="Should be 'COMPLETED'.")
    final_asset: FinalAssetInfo

class N8NErrorPayload(BaseModel):
    generation_request_id: uuid.UUID
    error_code: Optional[str] = None
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    failed_stage: Optional[str] = Field(None, description="e.g., 'sample_processing', 'final_processing'.")

# --- Error Schemas ---

class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    detail: Union[str, List[ErrorDetail]]

```