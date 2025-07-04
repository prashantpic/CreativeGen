import asyncio
import logging
from typing import List

from .providers.apns import APNSProvider
from .providers.fcm import FCMProvider
from ..base import NotificationChannel
from ...shared.schemas import NotificationPayload

logger = logging.getLogger(__name__)

class PushNotificationChannel(NotificationChannel):
    """
    Facade for sending mobile push notifications.

    This class implements the NotificationChannel interface for push notifications.
    It acts as a facade, delegating the actual sending to the appropriate
    provider (APNS or FCM) based on the device platform specified in the payload.
    It dispatches notifications to all devices concurrently using asyncio.
    """

    def __init__(self, apns_provider: APNSProvider, fcm_provider: FCMProvider):
        """
        Initializes the PushNotificationChannel.

        Args:
            apns_provider: An instance of the APNSProvider.
            fcm_provider: An instance of the FCMProvider.
        """
        self.apns_provider = apns_provider
        self.fcm_provider = fcm_provider
        logger.info("PushNotificationChannel initialized.")

    async def send(self, payload: NotificationPayload) -> None:
        """
        Sends push notifications to all devices listed in the payload.

        It determines the correct provider for each device and creates an
        asyncio task to send the notification. All tasks are run concurrently.

        Args:
            payload: The notification payload containing device list and data.
        """
        if not payload.devices:
            return

        # A robust way to get title and body from the data payload
        title = payload.data.get("title", payload.event_type.replace(".", " ").title())
        body = payload.data.get("message", "You have a new update.")
        
        tasks: List[asyncio.Task] = []
        for device in payload.devices:
            task = None
            token_preview = f"...{device.token[-6:]}"
            match device.platform:
                case "apns":
                    logger.info(f"Queueing APNS push for token {token_preview}")
                    task = asyncio.create_task(
                        self.apns_provider.send_push(device.token, title, body, payload.data)
                    )
                case "fcm":
                    logger.info(f"Queueing FCM push for token {token_preview}")
                    task = asyncio.create_task(
                        self.fcm_provider.send_push(device.token, title, body, payload.data)
                    )
                case _:
                    logger.warning(f"Unsupported push platform '{device.platform}' for token {token_preview}")
            
            if task:
                tasks.append(task)
        
        if not tasks:
            return

        logger.info(f"Dispatching {len(tasks)} push notifications concurrently.")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.error(f"A push notification failed during concurrent dispatch: {result}", exc_info=result)
        
        logger.info("Finished push notification dispatch cycle.")