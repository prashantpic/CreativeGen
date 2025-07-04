import asyncio
import logging
from fastapi import WebSocket
from typing import Dict, Set

logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    Manages active WebSocket connections in a thread-safe manner.

    This class acts as a singleton instance within the application to maintain
    a registry of all connected clients. It maps user IDs to a set of their
    active WebSocket connections, allowing for multiple connections per user
    (e.g., multiple browser tabs). An asyncio.Lock is used to prevent race
    conditions when modifying the shared connections dictionary.
    """
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, user_id: str, websocket: WebSocket):
        """

        Registers a new WebSocket connection for a given user.

        Args:
            user_id: The unique identifier of the user.
            websocket: The WebSocket object for the new connection.
        """
        async with self.lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()
            self.active_connections[user_id].add(websocket)
            logger.info(f"User '{user_id}' connected. Total connections for user: {len(self.active_connections[user_id])}")

    async def disconnect(self, user_id: str, websocket: WebSocket):
        """
        Removes a WebSocket connection for a given user.

        Args:
            user_id: The unique identifier of the user.
            websocket: The WebSocket object to disconnect.
        """
        async with self.lock:
            if user_id in self.active_connections:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    # Remove user entry if they have no more active connections
                    del self.active_connections[user_id]
                    logger.info(f"User '{user_id}' fully disconnected.")
                else:
                    logger.info(f"User '{user_id}' disconnected one session. Remaining: {len(self.active_connections[user_id])}")

    async def send_to_user(self, user_id: str, message: dict):
        """
        Sends a JSON message to all active WebSocket connections for a specific user.

        It iterates over a copy of the user's connection set to allow for safe
        modification of the original set during iteration if needed (e.g., a disconnect
        occurs while sending).

        Args:
            user_id: The ID of the target user.
            message: The JSON-serializable message dictionary to send.
        """
        if user_id in self.active_connections:
            # Iterate over a copy of the set to avoid runtime errors if the set is modified
            connections = list(self.active_connections.get(user_id, []))
            if not connections:
                logger.warning(f"Attempted to send message to user '{user_id}' but no active connections found.")
                return

            logger.info(f"Sending message to user '{user_id}' across {len(connections)} connection(s).")
            
            # Use asyncio.gather to send to all connections concurrently
            send_tasks = [self._send_to_websocket(ws, message) for ws in connections]
            await asyncio.gather(*send_tasks)

    async def _send_to_websocket(self, websocket: WebSocket, message: dict):
        """Helper to send to a single websocket and handle errors."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            # This can happen if the connection is closed between the check and the send
            logger.warning(f"Failed to send message to a websocket: {e}")