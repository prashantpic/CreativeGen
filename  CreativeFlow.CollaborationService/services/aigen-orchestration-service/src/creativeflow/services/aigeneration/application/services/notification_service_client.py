import logging
from typing import Dict, Any, Optional
import httpx

from creativeflow.services.aigeneration.core.config import Settings

logger = logging.getLogger(__name__)

class NotificationServiceClient:
    """
    Client for interacting with the dedicated Notification Service.
    """
    def __init__(self, http_client: httpx.AsyncClient, settings: Settings):
        self._http_client = http_client
        self._base_url = str(settings.NOTIFICATION_SERVICE_API_URL)

    async def send_notification(
        self,
        user_id: str,
        message: str,
        notification_type: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Sends a notification request to the Notification Service.

        This method will log errors but not raise exceptions to prevent
        the main orchestration flow from being blocked by notification failures.
        """
        logger.info(f"Sending notification of type '{notification_type}' to user {user_id}.")
        request_body = {
            "user_id": user_id,
            "message": message,
            "notification_type": notification_type,
            "metadata": payload or {}
        }
        
        try:
            url = f"{self._base_url}/send"
            response = await self._http_client.post(url, json=request_body)
            response.raise_for_status()
            logger.info(f"Successfully sent notification to user {user_id}.")
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.error(
                f"Failed to send notification to user {user_id}. Error: {e}",
                exc_info=True,
                extra={"request_body": request_body}
            )