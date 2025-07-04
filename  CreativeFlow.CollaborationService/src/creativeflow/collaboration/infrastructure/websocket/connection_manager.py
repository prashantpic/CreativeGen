import logging
from collections import defaultdict
from typing import Dict, List, Optional

from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    Manages active WebSocket connections for collaborative sessions.

    This manager maintains a registry of active connections within a single
    service instance, mapping them to users and collaboration sessions. It is
    responsible for handling connect/disconnect events and broadcasting messages
    to relevant clients.

    For scaling across multiple instances, this in-memory manager would work in
    conjunction with a Pub/Sub system (like `PubSubManager`) to broadcast
    messages to other instances, which would then use their own ConnectionManager
    to deliver the message to their local connections.
    """

    def __init__(self):
        # active_connections maps: session_id -> {user_id: WebSocket}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = defaultdict(dict)
        # Inverted map for quick lookup of user/session from a WebSocket object
        self.ws_to_user_map: Dict[WebSocket, tuple[str, str]] = {}

    async def connect(self, websocket: WebSocket, session_id: str, user_id: str):
        """
        Accepts and registers a new WebSocket connection.

        Args:
            websocket (WebSocket): The WebSocket instance from FastAPI.
            session_id (str): The ID of the collaboration session the user is joining.
            user_id (str): The ID of the user connecting.
        """
        await websocket.accept()
        self.active_connections[session_id][user_id] = websocket
        self.ws_to_user_map[websocket] = (session_id, user_id)
        logger.info("User '%s' connected to session '%s'. Total users in session: %d.",
                    user_id, session_id, len(self.active_connections[session_id]))

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the registry.

        Args:
            websocket (WebSocket): The WebSocket instance to disconnect.
        """
        if websocket in self.ws_to_user_map:
            session_id, user_id = self.ws_to_user_map[websocket]
            del self.ws_to_user_map[websocket]
            if session_id in self.active_connections and user_id in self.active_connections[session_id]:
                del self.active_connections[session_id][user_id]
                if not self.active_connections[session_id]:
                    # Clean up empty session entry
                    del self.active_connections[session_id]
                logger.info("User '%s' disconnected from session '%s'.", user_id, session_id)
            else:
                 logger.warning("User '%s' in session '%s' not found in active_connections during disconnect.",
                                user_id, session_id)
        else:
            logger.warning("Disconnected WebSocket not found in ws_to_user_map.")

    def get_user_info_for_connection(self, websocket: WebSocket) -> Optional[tuple[str, str]]:
        """
        Retrieves the session and user ID associated with a WebSocket connection.

        Args:
            websocket (WebSocket): The WebSocket instance.

        Returns:
            Optional[tuple[str, str]]: A tuple of (session_id, user_id) or None if not found.
        """
        return self.ws_to_user_map.get(websocket)

    def get_connections_for_session(self, session_id: str) -> List[WebSocket]:
        """
        Retrieves all active WebSocket connections for a given session.

        Args:
            session_id (str): The ID of the collaboration session.

        Returns:
            List[WebSocket]: A list of WebSocket instances for the session.
        """
        return list(self.active_connections.get(session_id, {}).values())

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Sends a message to a specific WebSocket connection.

        Args:
            message (str): The message to send.
            websocket (WebSocket): The target WebSocket connection.
        """
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error("Failed to send personal message: %s", e)
            self.disconnect(websocket) # Clean up potentially dead connection

    async def broadcast_to_session(self, message: str, session_id: str, exclude_websocket: Optional[WebSocket] = None):
        """
        Broadcasts a message to all clients in a specific session.

        Args:
            message (str): The message to broadcast.
            session_id (str): The ID of the target session.
            exclude_websocket (Optional[WebSocket]): A WebSocket to exclude from the broadcast
                                                     (typically the sender).
        """
        connections = self.active_connections.get(session_id, {})
        for user_id, connection in connections.items():
            if connection != exclude_websocket:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    # Connection might have closed unexpectedly
                    logger.error("Failed to broadcast to user '%s' in session '%s': %s", user_id, session_id, e)
                    # Disconnect the problematic client
                    self.disconnect(connection)

    async def broadcast_to_session_binary(self, data: bytes, session_id: str, exclude_websocket: Optional[WebSocket] = None):
        """
        Broadcasts binary data to all clients in a specific session.

        Args:
            data (bytes): The binary data to broadcast.
            session_id (str): The ID of the target session.
            exclude_websocket (Optional[WebSocket]): A WebSocket to exclude from the broadcast.
        """
        connections = self.active_connections.get(session_id, {})
        for user_id, connection in connections.items():
            if connection != exclude_websocket:
                try:
                    await connection.send_bytes(data)
                except Exception as e:
                    logger.error("Failed to broadcast binary data to user '%s' in session '%s': %s", user_id, session_id, e)
                    self.disconnect(connection)