import logging
import httpx
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class NotificationServiceClient:
    """
    Client for interacting with the dedicated Notification Service.
    """

    def __init__(self, http_client: httpx.AsyncClient, base_url: str):
        self._http_client = http_client
        self._base_url = base_url.rstrip('/')

    async def send_notification(
        self,
        user_id: str,
        message: str,
        notification_type: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Sends a notification request to the Notification Service.

        This method should not raise exceptions that would block the core
        generation flow. It logs errors and continues.

        Args:
            user_id: The ID of the user to notify.
            message: The main message content of the notification.
            notification_type: A category for the notification (e.g., "samples_ready").
            payload: Additional data to send with the notification (e.g., request_id).
        """
        url = f"{self._base_url}/send"
        notification_data = {
            "user_id": user_id,
            "message": message,
            "type": notification_type,
            "metadata": payload or {}
        }
        logger.info(f"Sending notification of type '{notification_type}' to user {user_id}.")

        try:
            response = await self._http_client.post(url, json=notification_data, timeout=5.0)
            
            # Check for non-2xx status codes
            if response.status_code >= 300:
                logger.error(
                    f"Failed to send notification to user {user_id}. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
        except httpx.RequestError as e:
            logger.error(f"Error sending notification to user {user_id}: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred while sending notification to user {user_id}.")