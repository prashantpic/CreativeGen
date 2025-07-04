"""
FastAPI router for managing social media connections (OAuth flows, listing,
disconnecting).
"""
import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse

from ....application.services import OAuthOrchestrationService
from ....dependencies import (get_current_user_id,
                            get_oauth_orchestration_service)
from ..schemas import common_schemas, connection_schemas

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/connect/{platform}",
    status_code=307,
    summary="Initiate OAuth Connection",
    operation_id="initiate_oauth_connection_connect__platform__get",
    responses={307: {"description": "Redirect to social platform for authorization."}},
)
async def initiate_oauth_connection(
    platform: str,
    request: Request,
    current_user_id: str = Depends(get_current_user_id),
    oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service),
):
    """
    Initiates the OAuth 2.0 connection flow for a given platform.

    This endpoint generates the authorization URL for the specified social
    platform and redirects the user's browser to it.
    """
    logger.info(
        "Initiating OAuth connection for user '%s' with platform '%s'",
        current_user_id,
        platform,
    )
    auth_url = await oauth_service.initiate_connection(
        platform=platform, user_id=current_user_id, request=request
    )
    return RedirectResponse(url=auth_url)


@router.get(
    "/connect/{platform}/callback",
    response_model=connection_schemas.SocialConnectionResponse,
    summary="Handle OAuth Callback",
    operation_id="handle_oauth_callback_connect__platform__callback_get",
)
async def handle_oauth_callback(
    platform: str,
    request: Request,
    code: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service),
):
    """
    Handles the OAuth 2.0 callback from the social platform after user
    authorization.

    It exchanges the authorization code for an access token, fetches user
    profile information, and securely stores the connection details.
    """
    # In a real app, the frontend would receive this response and likely
    # store tokens or redirect the user. We return the connection details.
    logger.info("Handling OAuth callback for platform '%s'", platform)
    
    callback_query = connection_schemas.OAuthCallbackQuery(code=code, error=error, state=state)

    connection = await oauth_service.finalize_connection(
        platform=platform, request=request, callback_query=callback_query
    )
    return connection_schemas.SocialConnectionResponse.model_validate(connection)


@router.get(
    "/",
    response_model=List[connection_schemas.SocialConnectionResponse],
    summary="List User Connections",
    operation_id="list_connections_get",
)
async def list_connections(
    current_user_id: str = Depends(get_current_user_id),
    oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service),
) -> List[connection_schemas.SocialConnectionResponse]:
    """
    Lists all active social media connections for the currently authenticated user.
    """
    logger.info("Fetching connections for user '%s'", current_user_id)
    connections = await oauth_service.get_user_connections(user_id=current_user_id)
    return [
        connection_schemas.SocialConnectionResponse.model_validate(c) for c in connections
    ]


@router.delete(
    "/{connection_id}",
    response_model=common_schemas.StatusResponse,
    summary="Disconnect Account",
    operation_id="disconnect_account__connection_id__delete",
)
async def disconnect_account(
    connection_id: UUID,
    current_user_id: str = Depends(get_current_user_id),
    oauth_service: OAuthOrchestrationService = Depends(get_oauth_orchestration_service),
) -> common_schemas.StatusResponse:
    """
    Disconnects a social media account.

    This operation revokes the stored OAuth tokens (if the platform API supports it)
    and deletes the connection record from the database.
    """
    logger.info(
        "Disconnecting account with ID '%s' for user '%s'",
        connection_id,
        current_user_id,
    )
    await oauth_service.disconnect(
        connection_id=connection_id, user_id=current_user_id
    )
    return common_schemas.StatusResponse(
        status="success", message="Account disconnected successfully."
    )