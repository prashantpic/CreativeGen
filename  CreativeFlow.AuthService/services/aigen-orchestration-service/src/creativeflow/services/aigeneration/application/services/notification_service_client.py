import logging
from typing import Optional, Dict, Any
import httpx
from pydantic import AnyUrl

logger = logging.getLogger(__name__)

class NotificationServiceClient:
    """
    Client for interacting with the dedicated Notification Service.
    """
    def __init__(self, base_url: AnyUrl, http_client: httpx.AsyncClient):
        self._base_url = str(base_url)
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
        Failures are logged but do not raise exceptions to avoid blocking
        the core generation workflow.
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
            response.raise_for_status()
            logger.debug(f"Successfully sent notification to user {user_id}.")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to send notification to user {user_id}. "
                f"Status: {e.response.status_code}, Response: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(
                f"Connection error while sending notification to user {user_id}. "
                f"URL: {e.request.url}, Error: {e}"
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred in NotificationServiceClient: {e}", exc_info=True)