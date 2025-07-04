"""
Central dispatcher for routing notifications to appropriate channels.

This module contains the `NotificationManager`, which is the core orchestrator
of the service. It receives a validated notification payload and, based on the
`target_channels` specified, directs the notification to the `WebSocketManager`
and/or the `PushNotificationService`.
"""

from creativeflow.services.notification.config import Settings
from creativeflow.services.notification.core.push_notification_service import PushNotificationService
from creativeflow.services.notification.core.schemas import NotificationPayload, PushNotificationContent, WebSocketMessage
from creativeflow.services.notification.core.websocket_manager import WebSocketManager
from creativeflow.services.notification.shared.exceptions import PushProviderError
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class NotificationManager:
    """
    Central dispatcher for notifications to WebSocket and Push channels.
    """

    def __init__(
        self,
        websocket_manager: WebSocketManager,
        push_service: PushNotificationService,
        settings: Settings
    ):
        """
        Initializes the NotificationManager with its dependencies.

        Args:
            websocket_manager: An instance of WebSocketManager.
            push_service: An instance of PushNotificationService.
            settings: The application settings.
        """
        self.websocket_manager = websocket_manager
        self.push_service = push_service
        self.settings = settings

    async def send_notification(self, payload: NotificationPayload):
        """
        Processes a notification payload and sends it to the specified target channels.

        Args:
            payload: The validated notification payload from the message queue.
        """
        logger.info(f"Processing notification for user '{payload.user_id}' with event type '{payload.event_type}'.")

        # --- WebSocket Dispatch ---
        if "websocket" in payload.target_channels:
            ws_message = WebSocketMessage(type=payload.event_type, content=payload.data)
            await self.websocket_manager.send_to_user(payload.user_id, ws_message)
            logger.info(f"Dispatched event '{payload.event_type}' to WebSocket for user '{payload.user_id}'.")

        # --- Push Notification Dispatch ---
        push_channels = [ch for ch in payload.target_channels if ch.startswith("push_")]
        if push_channels:
            device_token = payload.device_token or payload.data.get('device_token')
            if not device_token:
                logger.warning(f"Push notification requested for user '{payload.user_id}' but no device_token provided.")
                return

            try:
                # Construct a single push content object
                push_content = self._construct_push_content(payload)
                
                # Dispatch to iOS
                if "push_ios" in push_channels:
                    await self.push_service.send_push(
                        device_token=device_token,
                        device_type="ios",
                        content=push_content
                    )
                
                # Dispatch to Android
                if "push_android" in push_channels:
                    await self.push_service.send_push(
                        device_token=device_token,
                        device_type="android",
                        content=push_content
                    )

            except PushProviderError as e:
                # Errors are already logged in the PushNotificationService,
                # but we can add context here if needed.
                logger.error(f"Failed to dispatch push for user '{payload.user_id}': {e}")
            except Exception as e:
                logger.error(f"Unexpected error during push dispatch for user '{payload.user_id}': {e}")

    def _construct_push_content(self, payload: NotificationPayload) -> PushNotificationContent:
        """Helper to create a PushNotificationContent object from a payload."""
        # This logic could be expanded to map event_type to specific messages
        push_data = payload.data.get("push", {})
        return PushNotificationContent(
            title=push_data.get("title", "CreativeFlow Update"),
            body=push_data.get("body", "You have a new notification."),
            data=payload.data,
            deep_link_url=push_data.get("deep_link_url")
        )