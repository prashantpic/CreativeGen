"""
Service layer for managing user consents.
"""
from typing import Awaitable, List

from ...adapters.api.v1.schemas import ConsentUpdateRequestSchema
from ...application.schemas import ConsentSchema
from ...domain.models import Consent, ConsentType
from ...domain.repositories import IConsentRepository


class ConsentService:
    """
    Handles retrieval and updates of user consents for various
    processing activities.
    """

    def __init__(self, consent_repo: IConsentRepository):
        """
        Initializes the ConsentService.

        Args:
            consent_repo: The repository for consent data persistence.
        """
        self.consent_repo = consent_repo

    async def get_user_consents(self, auth_user_id: str) -> Awaitable[List[ConsentSchema]]:
        """
        Retrieves all consent records for a given user.

        Args:
            auth_user_id: The user's unique identifier.

        Returns:
            A list of consent DTOs.
        """
        consents = await self.consent_repo.get_all_by_user(auth_user_id)
        return [ConsentSchema.model_validate(c) for c in consents]

    async def update_user_consent(
        self,
        auth_user_id: str,
        consent_type: ConsentType,
        consent_update: ConsentUpdateRequestSchema,
    ) -> Awaitable[ConsentSchema]:
        """
        Updates a user's consent status for a specific type.

        This will create a new consent record if one does not already exist
        for the given user and consent type.

        Args:
            auth_user_id: The user's unique identifier.
            consent_type: The type of consent being updated.
            consent_update: The new state of the consent.

        Returns:
            The updated consent DTO.
        """
        consent = await self.consent_repo.get_by_user_and_type(
            auth_user_id=auth_user_id, consent_type=consent_type
        )

        if not consent:
            consent = Consent(
                auth_user_id=auth_user_id,
                consent_type=consent_type,
                version=consent_update.version,
            )

        if consent_update.is_granted:
            consent.grant(version=consent_update.version)
        else:
            consent.withdraw()

        saved_consent = await self.consent_repo.save(consent)
        return ConsentSchema.model_validate(saved_consent)