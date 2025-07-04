"""
Concrete implementation for communicating with the Notification Service.
Implements the INotificationService interface.
"""
import logging
from typing import Any, Dict
from uuid import UUID

import httpx

from ...app.interfaces import INotificationService

logger = logging.getLogger(__name__)


class HttpNotificationService(INotificationService):
    """
    Implements an HTTP client to trigger user notifications via the
    external Notification Service.
    """

    def __init__(self, http_client: httpx.AsyncClient, notification_service_url: str):
        self._http_client = http_client
        self._base_url = notification_service_url

    async def notify_user(self, user_id: UUID, message: Dict[str, Any]) -> None:
        """
        Makes a fire-and-forget asynchronous HTTP POST request to the
        Notification Service's API endpoint.
        """
        url = f"{self._base_url}/api/v1/notify"
        payload = {
            "user_id": str(user_id),
            "payload": message,
        }
        try:
            await self._http_client.post(url, json=payload, timeout=3.0)
            logger.info(f"Successfully sent notification request for user {user_id}")
        except httpx.RequestError as e:
            # Log the failure but do not re-raise the exception, as notifications
            # should not block the primary workflow.
            logger.error(
                f"Failed to send notification for user {user_id}. Error: {e}",
                exc_info=True
            )