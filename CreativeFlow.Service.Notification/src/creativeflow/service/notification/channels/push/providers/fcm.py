import logging
from typing import Any, Dict
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError

from .base import PushProvider
from .....core.config import Settings

logger = logging.getLogger(__name__)

class FCMProvider(PushProvider):
    """
    Adapter for sending push notifications via Firebase Cloud Messaging (FCM).

    This class encapsulates the specifics of the `firebase-admin` SDK, adapting it
    to the common `PushProvider` interface. It handles SDK initialization and
    the construction of FCM-specific message objects.
    """

    def __init__(self, settings: Settings):
        """
        Initializes the FCMProvider and the Firebase Admin SDK.

        Args:
            settings: The application configuration object.
        """
        self.enabled = settings.FCM_ENABLED
        if not self.enabled:
            logger.warning("FCM is disabled by configuration.")
            return

        try:
            # firebase_admin.initialize_app() can be called multiple times safely
            # as long as the same app is not initialized more than once.
            # If no app is initialized, it initializes the default app.
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.FCM_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, {'projectId': settings.FCM_PROJECT_ID})
                logger.info("Firebase Admin SDK initialized for FCM.")
            else:
                logger.info("Firebase Admin SDK already initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {e}", exc_info=True)
            self.enabled = False

    async def send_push(self, device_token: str, title: str, body: str, data: Dict[str, Any]) -> None:
        """
        Sends a push notification to an Android device.

        Args:
            device_token: The FCM registration token.
            title: The notification title.
            body: The notification body text.
            data: A dictionary of custom data. FCM requires data values to be strings.
        """
        if not self.enabled:
            logger.warning("FCM send aborted: provider not enabled.")
            return

        # FCM's data payload requires all values to be strings.
        stringified_data = {k: str(v) for k, v in data.items()}

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=stringified_data,
            token=device_token,
        )

        try:
            logger.info(f"Sending FCM push to token ending '...{device_token[-6:]}'")
            # The firebase-admin send methods are synchronous.
            # For a high-load system, consider running in a thread pool executor.
            # e.g., await asyncio.to_thread(messaging.send, message)
            response = messaging.send(message)
            logger.info(f"Successfully sent FCM push. Message ID: {response}")
        except FirebaseError as e:
            logger.error(f"FCM push failed for token ...{device_token[-6:]}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"An unexpected error occurred during FCM push: {e}", exc_info=True)