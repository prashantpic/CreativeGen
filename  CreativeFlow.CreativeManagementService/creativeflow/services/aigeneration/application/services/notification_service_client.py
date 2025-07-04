import logging
from typing import Dict, Any, Optional
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
        payload: Optional[Dict[str, Any]] = None
    ):
        """
        Constructs a payload and sends a notification request.
        
        Errors are logged but do not raise exceptions to avoid blocking the main flow.
        """
        url = f"{self._base_url}/send"
        notification_payload = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {}
        }
        
        logger.info(f"Sending notification of type '{notification_type}' to user {user_id}.")
        
        try:
            response = await self._http_client.post(url, json=notification_payload)
            response.raise_for_status()
            logger.debug(f"Successfully sent notification to user {user_id}.")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Notification Service returned error {e.response.status_code} for user {user_id}. "
                f"Response: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(
                f"Failed to connect to Notification Service at {e.request.url} for user {user_id}: {e}"
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while sending notification for user {user_id}: {e}",
                exc_info=True
            )