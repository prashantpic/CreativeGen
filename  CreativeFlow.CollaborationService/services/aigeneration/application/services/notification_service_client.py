import logging
from typing import Dict, Any

import httpx
from functools import lru_cache
from fastapi import Depends

from creativeflow.services.aigeneration.core.config import settings

logger = logging.getLogger(__name__)

class NotificationServiceClient:
    """
    Client for sending notification requests to the dedicated Notification Service.
    """
    def __init__(self, base_url: str):
        self._http_client = httpx.AsyncClient(base_url=base_url, timeout=5.0)

    async def close(self):
        await self._http_client.aclose()
        
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        message: str,
        payload: Dict[str, Any] = None
    ) -> None:
        """
        Sends a notification request to the Notification Service.
        Errors are logged but do not raise exceptions to avoid blocking the main flow.
        """
        notification_data = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {}
        }
        try:
            response = await self._http_client.post("/notifications/send", json=notification_data)
            if response.status_code >= 400:
                logger.error(
                    f"Failed to send notification to user {user_id}. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
            else:
                logger.info(f"Successfully sent '{notification_type}' notification to user {user_id}.")
        except httpx.RequestError as e:
            logger.error(
                f"Could not connect to Notification Service to send notification for user {user_id}. "
                f"Error: {e}",
                exc_info=True
            )

@lru_cache()
def get_notification_service_client() -> NotificationServiceClient:
    """
    Dependency to get a singleton instance of the NotificationServiceClient.
    """
    return NotificationServiceClient(base_url=str(settings.NOTIFICATION_SERVICE_API_URL))