"""
Client for interacting with the dedicated Notification Service.

This client provides a simple interface to send notifications to users
by calling the external Notification Service API. It is designed to be
resilient, logging errors without interrupting the main application flow.
"""

import logging
from typing import Dict, Any, Optional

import httpx

logger = logging.getLogger(__name__)

class NotificationServiceClient:
    """
    Sends notification requests to the dedicated Notification Service.
    """

    def __init__(self, http_client: httpx.AsyncClient, base_url: str):
        """
        Initializes the NotificationServiceClient.

        Args:
            http_client: An instance of httpx.AsyncClient for making requests.
            base_url: The base URL of the Notification Service API.
        """
        self._http_client = http_client
        self._base_url = base_url

    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Constructs and sends a notification request to the Notification Service.

        This method is fire-and-forget. It logs any errors encountered during the
        request but does not raise exceptions, ensuring that notification failures
        do not block the core generation workflow.

        Args:
            user_id: The ID of the user to notify.
            notification_type: The type of notification (e.g., "samples_ready").
            message: The main content of the notification message.
            payload: Optional dictionary with additional data (e.g., links, IDs).
        """
        url = f"{self._base_url}/send"
        notification_data = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {}
        }
        
        logger.info(f"Sending notification of type '{notification_type}' to user '{user_id}'")

        try:
            response = await self._http_client.post(url, json=notification_data, timeout=5.0)
            response.raise_for_status()
            logger.debug(f"Successfully sent notification to user '{user_id}'")
        except httpx.RequestError as e:
            logger.error(
                f"Could not send notification to user '{user_id}'. "
                f"Request to Notification Service failed: {e}"
            )
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Could not send notification to user '{user_id}'. "
                f"Notification Service returned status {e.response.status_code}: {e.response.text}"
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while sending notification to user '{user_id}': {e}",
                exc_info=True
            )