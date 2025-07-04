import logging
from .manager import ConnectionManager
from ..base import NotificationChannel
from ...shared.schemas import NotificationPayload

logger = logging.getLogger(__name__)

class WebSocketChannel(NotificationChannel):
    """
    Concrete implementation of NotificationChannel for WebSockets.

    This class adapts the general `send` method of the NotificationChannel
    interface to the specific action of sending a real-time message to a
    user via the ConnectionManager.
    """

    def __init__(self, manager: ConnectionManager):
        """
        Initializes the WebSocketChannel.

        Args:
            manager: An instance of ConnectionManager to handle the active connections.
        """
        self.manager = manager
        logger.info("WebSocketChannel initialized.")

    async def send(self, payload: NotificationPayload) -> None:
        """
        Sends a notification to a user's active WebSocket connections.

        This method extracts the user ID and message data from the payload and
        delegates the sending logic to the ConnectionManager.

        Args:
            payload: The notification payload containing user ID and data.
        """
        user_id = payload.user_id
        data_to_send = {
            "event_type": payload.event_type,
            "data": payload.data
        }
        
        logger.info(f"Dispatching notification via WebSocket to user_id: {user_id}")
        await self.manager.send_to_user(user_id, data_to_send)