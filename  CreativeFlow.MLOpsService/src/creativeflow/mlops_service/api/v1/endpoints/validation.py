"""
FastAPI router for AI Model Validation and Security Scanning endpoints.

This module provides the API for initiating model validation processes
(security, functional, etc.) and retrieving the results.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1 import schemas
from creativeflow.mlops_service.core.security import verify_api_key
from creativeflow.mlops_service.database import get_db
from creativeflow.mlops_service.services.model_validation_service import ModelValidationService
from creativeflow.mlops_service.utils.exceptions import ValidationFailedException

router = APIRouter()
model_validation_service = ModelValidationService()

@router.post(
    "/versions/{version_id}/trigger",
    response_model=schemas.ValidationResultResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger a validation process for a model version",
    dependencies=[Depends(verify_api_key)],
)
async def trigger_model_validation(
    version_id: UUID,
    validation_config: schemas.ValidationRequestSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Trigger an asynchronous validation process for a specific model version.
    The response is returned immediately with a PENDING status, while the actual
    scans run in the background.
    """
    # Assuming user_id would be extracted from a JWT.
    user_id: Optional[UUID] = None
    return await model_validation_service.initiate_validation(
        db, background_tasks, version_id=version_id, validation_config=validation_config, user_id=user_id
    )


@router.get(
    "/results/{result_id}",
    response_model=schemas.ValidationResultResponseSchema,
    summary="Get the result of a specific validation run",
    dependencies=[Depends(verify_api_key)],
)
async def get_validation_result(
    result_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve the detailed results of a specific validation run by its ID."""
    result = await model_validation_service.get_validation_result_by_id(db, result_id=result_id)
    if not result:
        raise ValidationFailedException(f"Validation result with ID {result_id} not found.")
    return result


@router.get(
    "/versions/{version_id}/results",
    response_model=List[schemas.ValidationResultResponseSchema],
    summary="List all validation results for a model version",
    dependencies=[Depends(verify_api_key)],
)
async def list_validation_results_for_version(
    version_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve all historical validation results for a specific model version."""
    return await model_validation_service.get_results_for_version(db, version_id=version_id)