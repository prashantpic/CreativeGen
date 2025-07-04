"""
FastAPI router for AI Model and Model Version management endpoints.

This module defines the API endpoints for creating, reading, and managing
AI models and their versions, including handling model artifact uploads.
"""
import json
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1 import schemas
from creativeflow.mlops_service.core.security import verify_api_key
from creativeflow.mlops_service.database import get_db
from creativeflow.mlops_service.services.model_registry_service import ModelRegistryService
from creativeflow.mlops_service.services.model_upload_service import ModelUploadService
from creativeflow.mlops_service.utils.exceptions import ModelNotFoundException, ModelVersionNotFoundException


router = APIRouter()
model_registry_service = ModelRegistryService()
model_upload_service = ModelUploadService()

@router.post(
    "/",
    response_model=schemas.ModelResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new AI Model entry",
    dependencies=[Depends(verify_api_key)],
)
async def create_model(
    model_in: schemas.ModelCreateSchema,
    db: Session = Depends(get_db),
):
    """Create a new AI Model, which acts as a container for versions."""
    return await model_registry_service.create_model(db, model_in=model_in)


@router.get(
    "/{model_id}",
    response_model=schemas.ModelResponseSchema,
    summary="Retrieve an AI Model by ID",
    dependencies=[Depends(verify_api_key)],
)
async def get_model(
    model_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve details for a specific AI Model."""
    model = await model_registry_service.get_model_by_id(db, model_id=model_id)
    if not model:
        raise ModelNotFoundException(str(model_id))
    return model


@router.get(
    "/",
    response_model=List[schemas.ModelResponseSchema],
    summary="List all AI Models",
    dependencies=[Depends(verify_api_key)],
)
async def list_models(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Retrieve a paginated list of all AI Models."""
    return await model_registry_service.get_models(db, skip=skip, limit=limit)


@router.post(
    "/{model_id}/versions",
    response_model=schemas.ModelVersionResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new model version and upload its artifact",
    dependencies=[Depends(verify_api_key)],
)
async def create_model_version(
    model_id: UUID,
    version_details_str: str = Form(..., description="A JSON string of ModelVersionCreateSchema"),
    file: UploadFile = File(..., description="The model artifact file"),
    db: Session = Depends(get_db),
):
    """
    Create a new version for an existing AI Model.

    This endpoint accepts multipart/form-data with:
    - `version_details`: A JSON string representing the version's metadata.
    - `file`: The actual model artifact (e.g., .onnx, .zip).
    """
    try:
        details_dict = json.loads(version_details_str)
        version_in = schemas.ModelVersionCreateSchema(**details_dict)
    except (json.JSONDecodeError, TypeError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid JSON in version_details: {e}")

    # TODO: This is a bit of a hack. A better way might be to stream to a temp file
    # or use a library that gives a file-like object with a known size.
    file_contents = await file.read()
    file_size = len(file_contents)
    file.file.seek(0) # Reset file pointer after reading

    artifact_path = await model_upload_service.upload_model_artifact(
        file_stream=file.file,
        file_name=file.filename,
        model_id=model_id,
        version_string=version_in.version_string,
        content_type=file.content_type,
        file_length=file_size,
    )

    # Assuming user_id would be extracted from a JWT in a real-world scenario
    user_id: Optional[UUID] = None 
    return await model_registry_service.create_model_version(
        db, model_id=model_id, version_in=version_in, artifact_path=artifact_path, user_id=user_id
    )


@router.get(
    "/versions/{version_id}",
    response_model=schemas.ModelVersionResponseSchema,
    summary="Retrieve a specific AI Model Version",
    dependencies=[Depends(verify_api_key)],
)
async def get_model_version(
    version_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve details for a specific AI Model Version by its ID."""
    version = await model_registry_service.get_model_version_by_id(db, version_id=version_id)
    if not version:
        raise ModelVersionNotFoundException(str(version_id))
    return version


@router.get(
    "/{model_id}/versions",
    response_model=List[schemas.ModelVersionResponseSchema],
    summary="List all versions for a specific model",
    dependencies=[Depends(verify_api_key)],
)
async def list_model_versions(
    model_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Retrieve a paginated list of all versions for a given AI Model."""
    versions = await model_registry_service.get_versions_for_model(db, model_id=model_id, skip=skip, limit=limit)
    return versions


@router.patch(
    "/versions/{version_id}/status",
    response_model=schemas.ModelVersionResponseSchema,
    summary="Update the status of an AI Model Version",
    dependencies=[Depends(verify_api_key)],
)
async def update_model_version_status(
    version_id: UUID,
    status_update: schemas.ModelVersionStatusUpdateSchema,
    db: Session = Depends(get_db),
):
    """
    Update the lifecycle status of a model version (e.g., promote to production).
    This endpoint enforces valid state transitions.
    """
    updated_version = await model_registry_service.update_version_status(
        db, version_id=version_id, new_status=status_update.new_status
    )
    return updated_version