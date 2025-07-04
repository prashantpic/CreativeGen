import asyncio
import logging
from ..shared.schemas import NotificationPayload
from ..channels.websocket.channel import WebSocketChannel
from ..channels.push.channel import PushNotificationChannel

logger = logging.getLogger(__name__)

class NotificationDispatcher:
    """
    Central orchestrator for dispatching notifications.

    This class receives a validated NotificationPayload and routes it to all
    configured notification channels (e.g., WebSocket, Push) concurrently.
    It embodies the core logic of the service, decoupling the message consumption
    from the specific delivery mechanisms.
    """

    def __init__(self, websocket_channel: WebSocketChannel, push_channel: PushNotificationChannel):
        """
        Initializes the NotificationDispatcher with its available channels.

        Args:
            websocket_channel: The channel for sending real-time web notifications.
            push_channel: The channel for sending mobile push notifications.
        """
        self.websocket_channel = websocket_channel
        self.push_channel = push_channel
        logger.info("NotificationDispatcher initialized.")

    async def dispatch_notification(self, payload: NotificationPayload) -> None:
        """
        Dispatches a notification to all configured channels simultaneously.

        It creates asyncio tasks for each channel's `send` method and runs
        them using `asyncio.gather`. This ensures that a delay or failure in one
        channel does not block others.

        Args:
            payload: The validated notification data object.
        """
        logger.info(
            f"Dispatching notification for user '{payload.user_id}' (event: {payload.event_type})"
        )

        tasks = [
            asyncio.create_task(self.websocket_channel.send(payload)),
            asyncio.create_task(self.push_channel.send(payload)),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                channel_name = "WebSocketChannel" if i == 0 else "PushNotificationChannel"
                logger.error(
                    f"Error dispatching notification via {channel_name}: {result}",
                    exc_info=result
                )
        
        logger.info(f"Finished dispatch for user '{payload.user_id}' (event: {payload.event_type})")