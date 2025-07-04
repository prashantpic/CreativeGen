import logging
from pathlib import Path
from typing import Any, Dict

from apns2.client import APNsClient
from apns2.payload import Payload
from apns2.errors import APNsException

from .base import PushProvider
from .....core.config import Settings

logger = logging.getLogger(__name__)

class APNSProvider(PushProvider):
    """
    Adapter for sending push notifications via Apple Push Notification Service (APNS).

    This class encapsulates the specifics of the `apns2` library, adapting it
    to the common `PushProvider` interface. It handles client initialization from
    configuration and the construction of APNS-specific payloads.
    """

    def __init__(self, settings: Settings):
        """
        Initializes the APNSProvider and its client.

        Args:
            settings: The application configuration object.
        """
        self.settings = settings
        self.client: APNsClient | None = None

        if not self.settings.APNS_ENABLED:
            logger.warning("APNS is disabled by configuration.")
            return

        auth_key_path = Path(self.settings.APNS_AUTH_KEY_PATH)
        if not auth_key_path.is_file():
            logger.error(f"APNS auth key file not found at: {auth_key_path}")
            return
        
        try:
            self.client = APNsClient(
                team_id=self.settings.APNS_TEAM_ID,
                auth_key_id=self.settings.APNS_KEY_ID,
                auth_key_filepath=str(auth_key_path),
                use_sandbox=self.settings.APNS_USE_SANDBOX,
            )
            logger.info(f"APNSProvider initialized. Sandbox mode: {self.settings.APNS_USE_SANDBOX}")
        except Exception as e:
            logger.error(f"Failed to initialize APNSClient: {e}", exc_info=True)


    async def send_push(self, device_token: str, title: str, body: str, data: Dict[str, Any]) -> None:
        """
        Sends a push notification to an iOS device.

        Args:
            device_token: The APNS device token.
            title: The notification title.
            body: The notification body text.
            data: A dictionary of custom data to include in the push payload.
        """
        if not self.client:
            logger.warning("APNS send aborted: client not initialized or disabled.")
            return

        try:
            alert = {"title": title, "body": body}
            payload = Payload(
                alert=alert,
                sound="default",
                badge=1,
                mutable_content=1,
                custom=data,
            )
            
            topic = self.settings.APNS_TOPIC
            if not topic:
                logger.error("APNS send failed: APNS_TOPIC is not configured.")
                return

            logger.info(f"Sending APNS push to token ending '...{device_token[-6:]}'")
            # The apns2 library is synchronous, so we run it in a thread pool
            # to avoid blocking the asyncio event loop.
            # For simplicity here we call it directly, but in a high-load
            # system, this should be wrapped with `asyncio.to_thread`.
            self.client.send_notification(token_hex=device_token, notification=payload, topic=topic)
            logger.info(f"Successfully sent APNS push to token ...{device_token[-6:]}")

        except APNsException as e:
            logger.error(f"APNS push failed for token ...{device_token[-6:]}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"An unexpected error occurred during APNS push: {e}", exc_info=True)