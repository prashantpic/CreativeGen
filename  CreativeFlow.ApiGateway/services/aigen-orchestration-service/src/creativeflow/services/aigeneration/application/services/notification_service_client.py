import logging
from typing import Dict, Any

import httpx

logger = logging.getLogger(__name__)

class NotificationServiceClient:
    """
    Client for sending notification requests to the dedicated Notification Service.
    """
    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url
        self._http_client = http_client

    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        message: str,
        payload: Dict[str, Any] = None
    ) -> None:
        """
        Sends a notification request to the Notification Service.

        This method will log errors if notification sending fails but will not
        raise an exception that would block the core generation flow.
        """
        notification_payload = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {}
        }
        
        try:
            url = f"{self._base_url}/send" # Assuming a `/send` endpoint
            logger.info(f"Sending notification of type '{notification_type}' to user {user_id}.")
            response = await self._http_client.post(url, json=notification_payload, timeout=5.0)
            response.raise_for_status()
            logger.info(f"Successfully sent notification to user {user_id}.")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to send notification to user {user_id}. "
                f"Notification Service returned status {e.response.status_code}: {e.response.text}",
                exc_info=True
            )
        except httpx.RequestError as e:
            logger.error(
                f"Could not connect to Notification Service to send notification to user {user_id}: {e}",
                exc_info=True
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while sending notification to user {user_id}: {e}",
                exc_info=True
            )