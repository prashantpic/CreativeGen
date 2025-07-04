import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from creativeflow.service.api.v1.dependencies import get_current_api_client, verify_usage_quota
from creativeflow.service.api.v1.schemas.generation_schemas import (
    GenerationRequestSchema,
    GenerationResponseSchema,
    GenerationStatusSchema
)
from creativeflow.service.db.models.api_client import APIClient
from creativeflow.service.integrations.aigen_orchestration_client import AIGenOrchClient

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=GenerationResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Initiate a Creative Generation Job",
    description="Submits a request to generate a creative asset. This is an asynchronous operation."
)
async def initiate_generation(
    request_data: GenerationRequestSchema,
    api_client: APIClient = Depends(verify_usage_quota),
    aigen_client: AIGenOrchClient = Depends()
) -> GenerationResponseSchema:
    """
    Endpoint to start a new AI generation job.

    - **Authentication**: Requires a valid API Key.
    - **Authorization**: Checks usage quotas and rate limits.
    - **Action**: Forwards the generation request to the AI Orchestration service.
    - **Response**: Returns a job ID for tracking the asynchronous task.
    """
    logger.info(f"Initiating generation for user {api_client.user_id} via API client {api_client.id}")
    try:
        response_data = await aigen_client.initiate_generation(
            request_data=request_data,
            user_id=api_client.user_id,
            api_client_id=api_client.id
        )
        return GenerationResponseSchema(**response_data)
    except Exception as e:
        logger.error(
            f"Failed to initiate generation for user {api_client.user_id}: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The generation service is currently unavailable. Please try again later."
        )


@router.get(
    "/{job_id}",
    response_model=GenerationStatusSchema,
    status_code=status.HTTP_200_OK,
    summary="Get Generation Job Status",
    description="Retrieves the current status and results of a generation job."
)
async def get_generation_status(
    job_id: uuid.UUID,
    api_client: APIClient = Depends(get_current_api_client),
    aigen_client: AIGenOrchClient = Depends()
) -> GenerationStatusSchema:
    """
    Endpoint to check the status of an ongoing or completed generation job.

    - **Authentication**: Requires a valid API Key.
    - **Authorization**: Ensures the job belongs to the authenticated user's account.
    - **Action**: Queries the AI Orchestration service for the job status.
    """
    logger.info(f"Fetching status for job {job_id} for user {api_client.user_id}")
    try:
        # The orchestration client should handle authorization (i.e., can this user see this job?)
        status_data = await aigen_client.get_generation_status(
            job_id=job_id,
            user_id=api_client.user_id
        )
        if status_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Generation job with ID '{job_id}' not found."
            )
        return GenerationStatusSchema(**status_data)
    except HTTPException as e:
        # Re-raise known HTTP exceptions
        raise e
    except Exception as e:
        logger.error(
            f"Failed to get status for job {job_id} for user {api_client.user_id}: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The generation service is currently unavailable. Please try again later."
        )