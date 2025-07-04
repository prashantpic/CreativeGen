import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class NotificationServiceClient:
    """
    Client for sending notification requests to the dedicated Notification Service.
    """

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url.rstrip('/')
        self._http_client = http_client

    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Sends a notification request to the Notification Service.
        This operation is "fire and forget". Errors are logged but do not
        raise exceptions that would halt the primary orchestration flow.
        """
        url = f"{self._base_url}/notifications"
        notification_data = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {}
        }
        
        logger.info(f"Sending notification of type '{notification_type}' to user {user_id}.")
        
        try:
            response = await self._http_client.post(url, json=notification_data, timeout=5.0)
            # Check for non-2xx responses but don't raise HTTPError to avoid breaking the caller
            if response.status_code >= 300:
                logger.error(
                    f"Notification Service returned a non-success status: {response.status_code}. "
                    f"Response: {response.text}"
                )
        except httpx.RequestError as e:
            logger.error(f"Could not connect to Notification Service at {url}: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred while sending a notification to user {user_id}.")