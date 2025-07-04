"""
Service layer for managing data privacy requests (GDPR/CCPA).
"""
from typing import Awaitable, List
from uuid import UUID
import logging

from ...application.schemas import (ConsentSchema, DataPrivacyRequestSchema,
                                    UserProfileDataExportSchema)
from ...domain.exceptions import ProfileNotFoundError
from ...domain.models import DataPrivacyRequest, DataPrivacyRequestType
from ...domain.repositories import (IConsentRepository,
                                    IDataPrivacyRequestRepository,
                                    IUserProfileRepository)

logger = logging.getLogger(__name__)

class DataPrivacyService:
    """
    Manages data subject requests for access, portability, and deletion
    of personal data. Orchestrates data deletion/anonymization.
    """

    def __init__(
        self,
        user_profile_repo: IUserProfileRepository,
        privacy_request_repo: IDataPrivacyRequestRepository,
        consent_repo: IConsentRepository,
    ):
        """
        Initializes the DataPrivacyService.

        Args:
            user_profile_repo: Repository for user profile data.
            privacy_request_repo: Repository for data privacy requests.
            consent_repo: Repository for user consent data.
        """
        self.user_profile_repo = user_profile_repo
        self.privacy_request_repo = privacy_request_repo
        self.consent_repo = consent_repo

    async def _create_request(
        self, auth_user_id: str, request_type: DataPrivacyRequestType
    ) -> Awaitable[DataPrivacyRequestSchema]:
        """
        Creates and saves a new data privacy request.

        Args:
            auth_user_id: The user's unique identifier.
            request_type: The type of request to create.

        Returns:
            The created data privacy request DTO.
        """
        request = DataPrivacyRequest(auth_user_id=auth_user_id, request_type=request_type)
        saved_request = await self.privacy_request_repo.save(request)
        logger.info(f"Created data privacy request {saved_request.id} of type {request_type} for user {auth_user_id}")
        # In a real system, this would likely trigger an async background task.
        return DataPrivacyRequestSchema.model_validate(saved_request)

    async def request_data_access(self, auth_user_id: str) -> Awaitable[DataPrivacyRequestSchema]:
        """Initiates a data access request for a user."""
        return await self._create_request(auth_user_id, DataPrivacyRequestType.ACCESS)

    async def request_data_portability(self, auth_user_id: str) -> Awaitable[DataPrivacyRequestSchema]:
        """Initiates a data portability request for a user."""
        return await self._create_request(auth_user_id, DataPrivacyRequestType.PORTABILITY)

    async def request_account_deletion(self, auth_user_id: str) -> Awaitable[DataPrivacyRequestSchema]:
        """Initiates an account deletion request for a user."""
        return await self._create_request(auth_user_id, DataPrivacyRequestType.DELETION)

    async def fulfill_data_access_request(
        self, auth_user_id: str
    ) -> Awaitable[UserProfileDataExportSchema]:
        """
        Compiles and returns the data for a user's access request.

        Args:
            auth_user_id: The user's unique identifier.

        Returns:
            A DTO containing the user's profile and consent data.
        """
        profile = await self.user_profile_repo.get_by_auth_id(auth_user_id)
        if not profile:
            raise ProfileNotFoundError(f"Profile for auth_user_id {auth_user_id} not found.")

        consents = await self.consent_repo.get_all_by_user(auth_user_id)

        export_data = UserProfileDataExportSchema(
            profile=profile,
            consents=[ConsentSchema.model_validate(c) for c in consents]
        )
        return export_data

    async def process_pending_deletion_requests_internal(self) -> Awaitable[None]:
        """
        Processes all pending deletion requests.

        This is an internal method intended to be run by a scheduled job.
        It finds pending deletion requests, anonymizes the associated user data,
        and updates the request status.
        """
        logger.info("Starting processing of pending deletion requests...")
        pending_requests = await self.privacy_request_repo.get_by_user_and_type(
            auth_user_id=None, # A real implementation would need to fetch all pending requests
            request_type=DataPrivacyRequestType.DELETION,
            status=DataPrivacyRequestStatus.PENDING,
        )

        for request in pending_requests:
            logger.info(f"Processing deletion request {request.id} for user {request.auth_user_id}")
            try:
                request.mark_as_processing()
                await self.privacy_request_repo.update(request)
                
                profile = await self.user_profile_repo.get_by_auth_id(request.auth_user_id)
                if profile:
                    profile.anonymize()
                    await self.user_profile_repo.save(profile)
                    logger.info(f"Anonymized profile for user {request.auth_user_id}")
                else:
                    logger.warning(f"Profile for user {request.auth_user_id} not found during deletion processing.")

                request.mark_as_completed()
                await self.privacy_request_repo.update(request)
                logger.info(f"Completed deletion request {request.id}")
            except Exception as e:
                logger.error(f"Failed to process deletion request {request.id}: {e}", exc_info=True)
                request.mark_as_failed(str(e))
                await self.privacy_request_repo.update(request)
        logger.info("Finished processing pending deletion requests.")