"""
FastAPI router for publishing and scheduling content to social media platforms.
"""
import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from ....application.services import PublishingOrchestrationService
from ....dependencies import (get_current_user_id,
                            get_publishing_orchestration_service)
from ..schemas import publishing_schemas

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/publish",
    response_model=publishing_schemas.PublishJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Publish Content Now",
    operation_id="publish_content_now_publish_post",
)
async def publish_content_now(
    payload: publishing_schemas.PublishRequest,
    current_user_id: str = Depends(get_current_user_id),
    publishing_service: PublishingOrchestrationService = Depends(
        get_publishing_orchestration_service
    ),
):
    """
    Accepts content and publishes it immediately to a connected social account.

    This is an asynchronous operation. The endpoint accepts the job and returns
    a job response. The actual publishing happens in the background.
    """
    logger.info(
        "Received request to publish now from user '%s' to connection '%s'",
        current_user_id,
        payload.connection_id,
    )
    job = await publishing_service.publish_now(
        user_id=current_user_id, payload=payload
    )
    return publishing_schemas.PublishJobResponse.model_validate(job, from_attributes=True)


@router.post(
    "/schedule",
    response_model=publishing_schemas.PublishJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Schedule Content",
    operation_id="schedule_content_schedule_post",
)
async def schedule_content(
    payload: publishing_schemas.ScheduleRequest,
    current_user_id: str = Depends(get_current_user_id),
    publishing_service: PublishingOrchestrationService = Depends(
        get_publishing_orchestration_service
    ),
):
    """
    Schedules content for future publishing to a connected social account.

    The service will create a scheduled job, which will be picked up and
    executed at the specified time by a background worker.
    """
    logger.info(
        "Received request to schedule content from user '%s' to connection '%s' for time '%s'",
        current_user_id,
        payload.connection_id,
        payload.schedule_time,
    )
    job = await publishing_service.schedule_publish(
        user_id=current_user_id, payload=payload
    )
    return publishing_schemas.PublishJobResponse.model_validate(job, from_attributes=True)


@router.get(
    "/jobs/{job_id}/status",
    response_model=publishing_schemas.PublishJobResponse,
    summary="Get Publish Job Status",
    operation_id="get_publish_job_status_jobs__job_id__status_get",
)
async def get_publish_job_status(
    job_id: UUID,
    current_user_id: str = Depends(get_current_user_id),
    publishing_service: PublishingOrchestrationService = Depends(
        get_publishing_orchestration_service
    ),
):
    """
    Retrieves the status and details of a specific publishing job.
    """
    logger.debug(
        "Fetching status for job '%s' for user '%s'", job_id, current_user_id
    )
    job = await publishing_service.get_job_status(
        job_id=job_id, user_id=current_user_id
    )
    return publishing_schemas.PublishJobResponse.model_validate(job, from_attributes=True)


@router.get(
    "/jobs",
    response_model=List[publishing_schemas.PublishJobResponse],
    summary="List Publishing Jobs",
    operation_id="list_publish_jobs_jobs_get",
)
async def list_publish_jobs(
    current_user_id: str = Depends(get_current_user_id),
    publishing_service: PublishingOrchestrationService = Depends(
        get_publishing_orchestration_service
    ),
    platform: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """
    Lists publishing jobs for the current user, with optional filters for
    platform and status.
    """
    logger.debug(
        "Listing jobs for user '%s' with filters: platform=%s, status=%s",
        current_user_id,
        platform,
        status,
    )
    jobs = await publishing_service.list_jobs(
        user_id=current_user_id, platform=platform, status=status
    )
    return [publishing_schemas.PublishJobResponse.model_validate(j, from_attributes=True) for j in jobs]