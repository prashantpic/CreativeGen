import logging
from typing import Optional, Dict, Any

import httpx

logger = logging.getLogger(__name__)


class NotificationServiceClient:
    """
    Client for interacting with the dedicated Notification Service.
    It provides an interface to send notifications to users.
    """

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        """
        Initializes the NotificationServiceClient.

        Args:
            base_url: The base URL of the Notification Service API.
            http_client: An instance of httpx.AsyncClient for making requests.
        """
        self._base_url = base_url.rstrip('/')
        self._http_client = http_client

    async def send_notification(
        self,
        user_id: str,
        message: str,
        notification_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Sends a notification request to the Notification Service.

        This method sends the request and logs any errors. It is designed to be
        'fire-and-forget' and will not raise exceptions that would block the
        core generation flow.

        Args:
            user_id: The ID of the user to notify.
            message: The main content of the notification message.
            notification_type: The type of notification (e.g., 'samples_ready').
            metadata: Optional dictionary with additional data for the notification.
        """
        url = f"{self._base_url}/notifications"
        payload = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": metadata or {}
        }
        
        try:
            response = await self._http_client.post(url, json=payload)
            
            # Check for non-successful status codes and log them.
            if response.status_code >= 400:
                logger.error(
                    f"Notification service returned an error. "
                    f"Status: {response.status_code}, "
                    f"Response: {response.text}, "
                    f"Payload: {payload}"
                )
            else:
                logger.info(f"Successfully sent notification of type '{notification_type}' to user '{user_id}'.")

        except httpx.RequestError as e:
            logger.error(
                f"Could not connect to notification service at {e.request.url!r}. "
                f"Failed to send notification to user '{user_id}'. "
                f"Error: {e}"
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while sending notification to user '{user_id}'. Error: {e}",
                exc_info=True
            )