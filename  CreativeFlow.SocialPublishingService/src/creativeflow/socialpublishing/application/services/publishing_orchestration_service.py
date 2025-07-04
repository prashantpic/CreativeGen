"""
Orchestrates the publishing and scheduling of content to social media platforms.
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from ....api.v1.schemas import publishing_schemas
from ....config import Settings
from ....domain.models import PublishJob, PublishJobStatus
from ....domain.repositories import IPublishJobRepository
from ....domain.services import PlatformPolicyValidator
from ...infrastructure.clients.base_social_client import BaseSocialClient
from ..exceptions import (ConnectionNotFoundError, ContentValidationError,
                        JobNotFoundError, PermissionDeniedError,
                        PublishingError)
from .oauth_orchestration_service import OAuthOrchestrationService

logger = logging.getLogger(__name__)


class PublishingOrchestrationService:
    """
    Handles the logic for publishing content immediately or scheduling it
    for later to various social platforms.
    """

    def __init__(
        self,
        publish_job_repo: IPublishJobRepository,
        oauth_service: OAuthOrchestrationService,
        policy_validator: PlatformPolicyValidator,
        config: Settings,
        platform_clients: Dict[str, BaseSocialClient],
    ):
        self.repo = publish_job_repo
        self.oauth_service = oauth_service
        self.policy_validator = policy_validator
        self.config = config
        self.platform_clients = platform_clients

    def _get_platform_client(self, platform: str) -> BaseSocialClient:
        client = self.platform_clients.get(platform.lower())
        if not client:
            raise PublishingError(f"Platform '{platform}' is not supported.")
        return client

    async def _execute_publish(
        self, job: PublishJob, access_token: str
    ):
        """Internal method to perform the actual publishing action."""
        job.increment_attempts()
        job.mark_as_processing()
        await self.repo.save(job)
        
        client = self._get_platform_client(job.platform)
        try:
            post_url = await client.publish_content(
                access_token=access_token,
                text=job.content_text,
                assets=job.asset_urls, # In a real app, this would be the schema object
                options=job.platform_specific_options
            )
            job.mark_as_published(post_url)
            logger.info("Successfully published job %s. Post URL: %s", job.id, post_url)
        except ContentValidationError as e:
             job.mark_as_content_rejected(str(e))
             logger.warning("Content for job %s rejected by platform: %s", job.id, e)
        except Exception as e:
            job.mark_as_failed(str(e))
            logger.error("Failed to publish job %s: %s", job.id, e, exc_info=True)
        
        await self.repo.save(job)

    async def publish_now(
        self, user_id: str, payload: publishing_schemas.PublishRequest
    ) -> PublishJob:
        """Creates a job and immediately attempts to publish it."""
        connection = await self.oauth_service.repo.get_by_id(payload.connection_id)
        if not connection or connection.user_id != user_id:
            raise ConnectionNotFoundError("Invalid connection ID provided.")
            
        is_valid, reason = await self.policy_validator.validate_content_for_platform(
            platform=connection.platform,
            content_text=payload.text_content,
            assets=payload.assets
        )
        if not is_valid:
            raise ContentValidationError(reason)

        job = PublishJob(
            id=uuid4(),
            user_id=user_id,
            social_connection_id=payload.connection_id,
            platform=connection.platform,
            content_text=payload.text_content,
            asset_urls=[asset.url for asset in payload.assets],
            platform_specific_options=payload.platform_specific_options,
            status=PublishJobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        await self.repo.save(job)
        
        # This is where you would trigger a background task.
        # For simplicity in this SDS, we'll run it in-process with asyncio.
        async def background_publish():
            try:
                token = await self.oauth_service.get_valid_access_token(payload.connection_id, user_id)
                await self._execute_publish(job, token)
            except Exception as e:
                job.mark_as_failed(f"Pre-flight check failed: {e}")
                await self.repo.save(job)
                logger.error("Error during background publish trigger for job %s: %s", job.id, e)

        asyncio.create_task(background_publish())

        return job

    async def schedule_publish(
        self, user_id: str, payload: publishing_schemas.ScheduleRequest
    ) -> PublishJob:
        """Creates a job to be published at a future time."""
        connection = await self.oauth_service.repo.get_by_id(payload.connection_id)
        if not connection or connection.user_id != user_id:
            raise ConnectionNotFoundError("Invalid connection ID provided.")

        is_valid, reason = await self.policy_validator.validate_content_for_platform(
            platform=connection.platform,
            content_text=payload.text_content,
            assets=payload.assets
        )
        if not is_valid:
            raise ContentValidationError(reason)

        job = PublishJob(
            id=uuid4(),
            user_id=user_id,
            social_connection_id=payload.connection_id,
            platform=connection.platform,
            content_text=payload.text_content,
            asset_urls=[asset.url for asset in payload.assets],
            platform_specific_options=payload.platform_specific_options,
            status=PublishJobStatus.SCHEDULED,
            scheduled_at=payload.schedule_time,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        await self.repo.save(job)
        logger.info("Successfully scheduled job %s for %s", job.id, job.scheduled_at)
        return job

    async def get_job_status(self, job_id: str, user_id: str) -> PublishJob:
        job = await self.repo.get_by_id(job_id)
        if not job:
            raise JobNotFoundError(f"Job with ID '{job_id}' not found.")
        if job.user_id != user_id:
            raise PermissionDeniedError("User does not own this job.")
        return job

    async def list_jobs(
        self, user_id: str, platform: Optional[str], status: Optional[str]
    ) -> List[PublishJob]:
        return await self.repo.list_by_user_id(
            user_id=user_id, platform=platform, status=status
        )