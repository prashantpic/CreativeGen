"""
Client for sending push notifications via Firebase Cloud Messaging (FCM).

This module implements the `BasePushProvider` interface for FCM, using the
`pyfcm` library to communicate with Google's servers. It handles the construction
of FCM-specific payloads and manages the connection to the service.
"""
import asyncio
from typing import Optional

from pyfcm import FCMNotification

from creativeflow.services.notification.channels.push.base_push_provider import BasePushProvider
from creativeflow.services.notification.config import Settings
from creativeflow.services.notification.core.schemas import PushNotificationContent
from creativeflow.services.notification.shared.exceptions import PushProviderError
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class FCMClient(BasePushProvider):
    """
    An adapter for sending push notifications to Android devices using FCM.
    """

    def __init__(self, config: Settings):
        """
        Initializes the FCMClient.

        Args:
            config: The application settings containing the FCM API key.
        """
        self.config = config
        self.fcm_service_instance: Optional[FCMNotification] = None

        if self.config.ENABLE_FCM_PUSH:
            try:
                if not self.config.FCM_API_KEY:
                    raise ValueError("FCM_API_KEY is not configured.")
                self.fcm_service_instance = FCMNotification(api_key=self.config.FCM_API_KEY)
                logger.info("FCM client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize FCM client: {e}")
                self.fcm_service_instance = None

    async def send(self, device_token: str, payload: PushNotificationContent) -> None:
        """
        Sends a push notification to an Android device via FCM.

        Args:
            device_token: The FCM registration ID.
            payload: The structured content for the notification.

        Raises:
            PushProviderError: If the notification fails to send.
        """
        if not self.fcm_service_instance:
            logger.warning("FCM client is not initialized or is disabled. Skipping push notification.")
            return

        data_message = payload.data or {}
        if payload.deep_link_url:
            data_message['deep_link_url'] = payload.deep_link_url

        def _send_sync():
            return self.fcm_service_instance.notify_single_device(
                registration_id=device_token,
                message_title=payload.title,
                message_body=payload.body,
                data_message=data_message if data_message else None,
            )

        try:
            # pyfcm is synchronous, so we run it in a thread pool.
            result = await asyncio.to_thread(_send_sync)

            if result.get("success"):
                logger.info(f"FCM push sent successfully to token starting with {device_token[:8]}...")
            else:
                errors = result.get("results", [{}])[0].get("error")
                error_msg = f"FCM push failed: {result.get('failure')} failures. Error: {errors}"
                logger.error(error_msg)
                raise PushProviderError(provider_name="FCM", original_error=errors)

        except Exception as e:
            logger.error(f"An unexpected error occurred while sending FCM push: {e}")
            raise PushProviderError(provider_name="FCM", original_error=e)