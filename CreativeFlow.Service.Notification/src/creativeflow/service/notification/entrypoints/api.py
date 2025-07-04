import logging
from typing import Annotated

from fastapi import (
    APIRouter, 
    WebSocket, 
    WebSocketDisconnect, 
    Depends, 
    HTTPException, 
    status,
    Query
)

from ..channels.websocket.manager import ConnectionManager

logger = logging.getLogger(__name__)

# This is a placeholder for a real authentication dependency.
# In a real application, this would decode and validate a JWT.
async def get_current_user_from_token(token: Annotated[str | None, Query()] = None) -> str:
    """
    Simulates validating a token from a query parameter and extracting the user ID.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    # In a real app, you would decode the JWT and get the user ID (subject).
    # For this simulation, we'll assume the token is the user ID.
    user_id = token
    logger.debug(f"Authenticated user_id '{user_id}' from token.")
    return user_id


def create_api_router(connection_manager: ConnectionManager) -> APIRouter:
    """
    Factory function to create the API router and inject dependencies.
    This pattern makes testing easier and manages dependency lifecycle explicitly.
    """
    router = APIRouter()

    @router.get("/health", status_code=status.HTTP_200_OK)
    async def health_check():
        """A simple health check endpoint for monitoring."""
        return {"status": "ok"}


    @router.websocket("/ws")
    async def websocket_endpoint(
        websocket: WebSocket,
        token: Annotated[str | None, Query()] = None
    ):
        """
        Handles WebSocket connections for real-time notifications.
        Authentication is performed via a token in the query string.
        """
        user_id = None
        try:
            user_id = await get_current_user_from_token(token)
            await websocket.accept()
            await connection_manager.connect(user_id, websocket)
            
            # This loop is to keep the connection alive and detect disconnects.
            # The service primarily sends messages, not receives them.
            while True:
                await websocket.receive_text()

        except WebSocketDisconnect:
            if user_id:
                await connection_manager.disconnect(user_id, websocket)
                logger.info(f"User '{user_id}' websocket disconnected.")
        except HTTPException:
            # This catches the auth error from get_current_user_from_token
            logger.warning("WebSocket connection rejected due to invalid or missing token.")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        except Exception as e:
            logger.error(f"An unexpected error occurred in the websocket endpoint: {e}", exc_info=True)
            if user_id:
                 await connection_manager.disconnect(user_id, websocket)

    return router