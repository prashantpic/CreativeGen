"""
Manager for handling active WebSocket connections.

This module provides the `WebSocketManager` class, which is responsible for
maintaining a state of all active client connections. It provides methods to
connect and disconnect clients, and to send messages to specific users or
broadcast to all connected clients. This manager is instance-local, meaning
it only knows about connections to the specific service instance where it runs.
"""
from collections import defaultdict
from typing import Dict, List

from fastapi import WebSocket

from creativeflow.services.notification.core.schemas import WebSocketMessage
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class WebSocketManager:
    """
    Manages WebSocket client connections on a per-instance basis.
    """

    def __init__(self):
        """Initializes the WebSocketManager."""
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, user_id: str):
        """
        Accepts a new WebSocket connection and adds it to the pool.

        Args:
            websocket: The WebSocket connection object from FastAPI.
            user_id: The ID of the user associated with this connection.
        """
        await websocket.accept()
        self.active_connections[user_id].append(websocket)
        logger.info(f"WebSocket connected for user: {user_id}. Total connections for user: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: str):
        """
        Removes a WebSocket connection from the pool.

        Args:
            websocket: The WebSocket connection object to remove.
            user_id: The ID of the user associated with the connection.
        """
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
                logger.info(f"WebSocket disconnected for user: {user_id}.")
            else:
                logger.warning(f"Attempted to disconnect a non-existent websocket for user {user_id}.")
        else:
            logger.warning(f"Attempted to disconnect websocket for a user {user_id} with no active connections.")

    async def send_to_user(self, user_id: str, message: WebSocketMessage):
        """
        Sends a message to all active connections for a specific user.

        It gracefully handles and cleans up any connections that have been
        unexpectedly closed.

        Args:
            user_id: The ID of the target user.
            message: The WebSocketMessage object to send.
        """
        if user_id in self.active_connections:
            connections = self.active_connections[user_id][:]  # Create a copy for safe iteration
            if not connections:
                return

            message_json = message.model_dump_json()
            disconnected_sockets = []

            for connection in connections:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    logger.warning(f"Failed to send to a WebSocket for user {user_id}, marking for removal. Error: {e}")
                    disconnected_sockets.append(connection)

            # Clean up disconnected sockets
            for sock in disconnected_sockets:
                self.disconnect(sock, user_id)
            
            logger.debug(f"Sent message of type '{message.type}' to {len(connections) - len(disconnected_sockets)} connections for user {user_id}.")

    async def broadcast(self, message: WebSocketMessage):
        """
        Sends a message to all connected clients. Use with caution.

        Args:
            message: The WebSocketMessage object to broadcast.
        """
        all_user_ids = list(self.active_connections.keys())
        message_json = message.model_dump_json()

        logger.info(f"Broadcasting message of type '{message.type}' to all users.")
        
        for user_id in all_user_ids:
            connections = self.active_connections.get(user_id, [])[:]
            disconnected_sockets = []
            for connection in connections:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    logger.warning(f"Failed to broadcast to a WebSocket for user {user_id}. Error: {e}")
                    disconnected_sockets.append(connection)

            for sock in disconnected_sockets:
                self.disconnect(sock, user_id)