"""
FastAPI WebSocket endpoints for client connections.

This module defines the WebSocket API routes for the notification service.
It handles the WebSocket connection lifecycle, including authentication,
connection management, and graceful disconnection.
"""
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status

from creativeflow.services.notification.core.websocket_manager import WebSocketManager
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# In a production environment, this would be a singleton managed by a
# dependency injection container. For this service's scope, a module-level
# instance is sufficient.
websocket_manager = WebSocketManager()


async def validate_token_and_get_user_id(token: str) -> str | None:
    """
    Placeholder for a real token validation function.

    In a real application, this would involve:
    1.  Decoding a JWT.
    2.  Verifying the signature and expiration.
    3.  Extracting the user ID from the claims.
    4.  Potentially querying a user service or cache to ensure the user exists.

    For this example, we'll use a simple mock validation.
    """
    if token and token.startswith("valid-token-for-user-"):
        return token.replace("valid-token-for-user-", "")
    return None


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="Authentication token for the user.")
):
    """
    WebSocket endpoint for real-time notifications.

    Clients must connect to this endpoint with a valid authentication token
    passed as a query parameter. The server will validate the token to
    associate the connection with a specific user.

    Example connection URL: wss://your-domain.com/ws?token=valid-token-for-user-123
    """
    user_id = await validate_token_and_get_user_id(token)
    if not user_id:
        logger.warning("WebSocket connection attempt with invalid token.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket_manager.connect(websocket, user_id)

    try:
        # Keep the connection alive and listen for any client messages (e.g., pings)
        while True:
            # We don't expect messages from the client in this service's design,
            # but `receive_text` is necessary to detect disconnection.
            data = await websocket.receive_text()
            logger.debug(f"Received text from user {user_id}: {data} (likely a ping)")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, user_id)
        logger.info(f"WebSocket for user {user_id} disconnected gracefully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred on WebSocket for user {user_id}: {e}")
        # Ensure cleanup on unexpected errors
        websocket_manager.disconnect(websocket, user_id)