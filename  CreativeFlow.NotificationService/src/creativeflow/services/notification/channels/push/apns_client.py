"""
Client for sending push notifications via Apple Push Notification Service (APNS).

This module implements the `BasePushProvider` interface for APNS, using the
`apns2` library to communicate with Apple's servers. It handles the construction
of APNS-specific payloads and manages the connection to the service.
"""
import asyncio
import os
from typing import Optional

from apns2.client import APNsClient, Notification
from apns2.payload import Payload

from creativeflow.services.notification.channels.push.base_push_provider import BasePushProvider
from creativeflow.services.notification.config import Settings
from creativeflow.services.notification.core.schemas import PushNotificationContent
from creativeflow.services.notification.shared.exceptions import PushProviderError
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class APNSClient(BasePushProvider):
    """
    An adapter for sending push notifications to iOS devices using APNS.
    """

    def __init__(self, config: Settings):
        """
        Initializes the APNSClient.

        Args:
            config: The application settings containing APNS credentials.
        """
        self.config = config
        self.apns_client_instance: Optional[APNsClient] = None

        if self.config.ENABLE_APNS_PUSH:
            try:
                cert_file = self.config.APNS_CERT_FILE
                if not cert_file or not os.path.exists(cert_file):
                     raise FileNotFoundError(f"APNS certificate file not found at path: {cert_file}")

                self.apns_client_instance = APNsClient(
                    key=cert_file,
                    use_sandbox=self.config.APNS_USE_SANDBOX,
                    team_id=self.config.APNS_TEAM_ID,
                    key_id=self.config.APNS_KEY_ID
                )
                logger.info("APNS client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize APNS client: {e}")
                self.apns_client_instance = None

    async def send(self, device_token: str, payload: PushNotificationContent) -> None:
        """
        Sends a push notification to an iOS device via APNS.

        Args:
            device_token: The APNS device token.
            payload: The structured content for the notification.

        Raises:
            PushProviderError: If the notification fails to send.
        """
        if not self.apns_client_instance:
            logger.warning("APNS client is not initialized or is disabled. Skipping push notification.")
            return

        custom_data = payload.data or {}
        if payload.deep_link_url:
            custom_data['deep_link_url'] = payload.deep_link_url

        apns_payload = Payload(
            alert={"title": payload.title, "body": payload.body},
            sound="default",
            badge=1,
            custom=custom_data
        )

        notification = Notification(payload=apns_payload, token=device_token)

        try:
            # apns2 is synchronous, so we run it in a thread pool.
            response = await asyncio.to_thread(
                self.apns_client_instance.send_notification, notification
            )

            if response.is_successful:
                logger.info(f"APNS push sent successfully to token starting with {device_token[:8]}...")
            else:
                error_msg = f"APNS push failed: {response.status_code} - {response.description}"
                logger.error(error_msg)
                raise PushProviderError(provider_name="APNS", original_error=response.description)

        except Exception as e:
            logger.error(f"An unexpected error occurred while sending APNS push: {e}")
            raise PushProviderError(provider_name="APNS", original_error=e)