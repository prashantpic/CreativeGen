import logging
from typing import Optional, Dict, Any

import httpx

logger = logging.getLogger(__name__)


class NotificationClient:
    """
    Client for the CreativeFlow Notification Service.
    
    This class is responsible for facilitating the sending of notifications
    (e.g., generation status updates) to users by making HTTP requests to the
    central Notification Service API.
    """

    def __init__(self, notification_service_url: str, http_client: httpx.AsyncClient):
        """
        Initializes the NotificationClient.

        Args:
            notification_service_url: The base URL for the Notification Service.
            http_client: An instance of httpx.AsyncClient for making asynchronous requests.
        """
        self._notification_service_url = notification_service_url.rstrip('/')
        self._http_client = http_client

    async def send_user_notification(
        self,
        user_id: str,
        notification_type: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Sends a notification to a user via the Notification Service.

        This method constructs the request payload and sends it to the Notification Service.
        It is designed to be resilient, logging errors without interrupting the calling process.

        Args:
            user_id: The unique identifier of the user to be notified.
            notification_type: A string indicating the category of the notification 
                               (e.g., 'generation_complete', 'billing_alert').
            message: The content of the notification message.
            payload: An optional dictionary containing additional contextual data,
                     such as a link to a generated asset or project.
        """
        endpoint = f"{self._notification_service_url}/notifications"
        request_body = {
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "metadata": payload or {}
        }
        
        try:
            response = await self._http_client.post(endpoint, json=request_body)
            
            if response.is_success:
                logger.info(f"Successfully sent notification of type '{notification_type}' to user '{user_id}'.")
            else:
                logger.error(
                    f"Notification service returned an error status: {response.status_code}. "
                    f"Response: {response.text}. "
                    f"Original payload: {request_body}"
                )
        except httpx.RequestError as e:
            logger.error(
                f"A network error occurred while trying to send a notification to user '{user_id}'. "
                f"Request URL: {e.request.url!r}. Error: {e}"
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred in the notification client for user '{user_id}'. Error: {e}",
                exc_info=True
            )