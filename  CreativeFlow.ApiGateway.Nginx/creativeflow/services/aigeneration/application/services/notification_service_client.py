import logging
from typing import Optional, Dict, Any
import httpx

from ...core.error_handlers import ExternalServiceError

class NotificationServiceClient:
    """
    Client for interacting with the dedicated Notification Service.
    """

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url
        self._http_client = http_client
        self.service_name = "Notification Service"

    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Sends a notification request to the Notification Service.
        This operation is "fire-and-forget" and will not block the main generation flow on failure.
        """
        url = f"{self._base_url}/send"
        notification_payload = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {},
        }
        
        try:
            logging.info(f"Sending notification '{notification_type}' to user {user_id}")
            response = await self._http_client.post(url, json=notification_payload)
            response.raise_for_status()
            logging.info(f"Successfully sent notification to user {user_id}")
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            # Log the error but do not raise an exception to prevent halting the core process.
            logging.error(f"Failed to send notification to user {user_id}. Error: {e}")