import logging
from typing import Dict, Any, Optional

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
        Failures are logged but do not raise exceptions to avoid blocking the main flow.
        """
        url = f"{self._base_url}/send"
        request_body = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {}
        }
        
        try:
            response = await self._http_client.post(url, json=request_body)
            response.raise_for_status()
            logger.info(
                "Successfully sent notification of type '%s' to user %s.",
                notification_type, user_id
            )
        except httpx.HTTPError as e:
            logger.error(
                "Failed to send notification to user %s. Status: %s, Response: %s",
                user_id,
                e.response.status_code if hasattr(e, 'response') else "N/A",
                e.response.text if hasattr(e, 'response') else "N/A",
                exc_info=True
            )
        except Exception as e:
            logger.error(
                "An unexpected error occurred while sending notification to user %s: %s",
                user_id, e, exc_info=True
            )