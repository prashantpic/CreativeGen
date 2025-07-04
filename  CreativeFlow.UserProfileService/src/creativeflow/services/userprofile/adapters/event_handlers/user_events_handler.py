"""
Handles incoming user-related events from other microservices.
"""
import logging

from ....application.services.data_privacy_service import DataPrivacyService

logger = logging.getLogger(__name__)


class UserEventsHandler:
    """
    Listens to events from other services (e.g., UserDeleted from Auth service)
    and triggers corresponding actions in this service.
    """

    def __init__(self, data_privacy_service: DataPrivacyService):
        """
        Initializes the event handler.

        Args:
            data_privacy_service: The service for handling data privacy tasks.
        """
        self.data_privacy_service = data_privacy_service

    async def handle_user_deleted_event(self, event_data: dict) -> None:
        """
        Handles a 'UserDeletedEvent' from an external service.

        This handler initiates the standard, auditable data deletion workflow
        by creating a formal deletion request, rather than deleting data directly.

        Args:
            event_data: The event payload, expected to contain 'auth_user_id'.
        """
        auth_user_id = event_data.get("auth_user_id")
        if not auth_user_id:
            logger.warning("Received UserDeletedEvent without 'auth_user_id'. Ignoring.")
            return

        logger.info(
            f"Received UserDeletedEvent for auth_user_id: {auth_user_id}. "
            f"Initiating account deletion request."
        )
        try:
            await self.data_privacy_service.request_account_deletion(auth_user_id)
            logger.info(
                f"Successfully initiated deletion request for auth_user_id: {auth_user_id}"
            )
        except Exception as e:
            logger.error(
                f"Failed to handle UserDeletedEvent for auth_user_id {auth_user_id}: {e}",
                exc_info=True,
            )