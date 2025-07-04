"""
Service for dispatching push notifications to the appropriate provider.

This module contains the `PushNotificationService`, which acts as a dispatcher.
It receives a generic push notification request and, based on the device type,
routes it to the correct client (APNS or FCM). This decouples the core logic
from the specific implementation details of each push provider.
"""

from creativeflow.services.notification.channels.push.apns_client import APNSClient
from creativeflow.services.notification.channels.push.fcm_client import FCMClient
from creativeflow.services.notification.config import Settings
from creativeflow.services.notification.core.schemas import PushNotificationContent
from creativeflow.services.notification.shared.exceptions import PushProviderError
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class PushNotificationService:
    """
    Dispatches push notifications to the appropriate provider based on device type.
    """

    def __init__(self, apns_client: APNSClient, fcm_client: FCMClient, settings: Settings):
        """
        Initializes the PushNotificationService with its dependencies.

        Args:
            apns_client: An instance of the APNSClient.
            fcm_client: An instance of the FCMClient.
            settings: The application settings.
        """
        self.apns_client = apns_client
        self.fcm_client = fcm_client
        self.settings = settings

    async def send_push(self, device_token: str, device_type: str, content: PushNotificationContent) -> None:
        """
        Sends a push notification by routing to the correct provider.

        Args:
            device_token: The unique token for the target device.
            device_type: The type of the device ('ios' or 'android').
            content: The structured content of the notification.
        
        Raises:
            PushProviderError: If the selected provider fails to send the notification.
        """
        logger.info(f"Attempting to send push to {device_type} device with token starting {device_token[:8]}...")
        device_type_lower = device_type.lower()

        try:
            if device_type_lower == "ios":
                if self.settings.ENABLE_APNS_PUSH:
                    await self.apns_client.send(device_token, content)
                else:
                    logger.info("APNS provider is disabled. Skipping notification.")
            elif device_type_lower == "android":
                if self.settings.ENABLE_FCM_PUSH:
                    await self.fcm_client.send(device_token, content)
                else:
                    logger.info("FCM provider is disabled. Skipping notification.")
            else:
                logger.warning(
                    f"Unsupported device_type '{device_type}' or provider disabled for token {device_token[:8]}..."
                )
        except PushProviderError as e:
            logger.error(f"Push dispatch failed for {device_type} token {device_token[:8]...}: {e}")
            # Re-raise to allow the caller (NotificationManager) to know about the failure.
            raise