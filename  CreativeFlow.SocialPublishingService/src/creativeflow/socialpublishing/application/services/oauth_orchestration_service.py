"""
Orchestrates OAuth 2.0 flows for connecting social media accounts. Handles
token exchange, storage, and retrieval.
"""
import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict
from uuid import uuid4

from fastapi import Request

from ....api.v1.schemas import connection_schemas
from ....config import Settings
from ....domain.models import SocialConnection
from ....domain.repositories import ISocialConnectionRepository
from ....domain.services import ITokenEncryptionService
from ...infrastructure.clients.base_social_client import BaseSocialClient
from ..exceptions import (ConnectionNotFoundError, OAuthConnectionError,
                        PermissionDeniedError, TokenEncryptionError,
                        TokenExpiredError)

logger = logging.getLogger(__name__)


class OAuthOrchestrationService:
    """
    Manages the entire lifecycle of OAuth connections for different social
    media platforms.
    """

    def __init__(
        self,
        social_connection_repo: ISocialConnectionRepository,
        token_encryption_service: ITokenEncryptionService,
        config: Settings,
        platform_clients: Dict[str, BaseSocialClient],
    ):
        self.repo = social_connection_repo
        self.encryption_service = token_encryption_service
        self.config = config
        self.platform_clients = platform_clients

    def _get_platform_client(self, platform: str) -> BaseSocialClient:
        client = self.platform_clients.get(platform.lower())
        if not client:
            raise OAuthConnectionError(f"Platform '{platform}' is not supported.")
        return client

    async def initiate_connection(
        self, platform: str, user_id: str, request: Request
    ) -> str:
        """
        Generates the authorization URL to initiate an OAuth 2.0 flow.
        """
        client = self._get_platform_client(platform)
        redirect_uri = str(
            request.url_for(
                "handle_oauth_callback_connect__platform__callback_get",
                platform=platform,
            )
        )
        # State should securely store user_id and a CSRF token
        csrf_token = secrets.token_hex(16)
        state = f"{user_id}:{csrf_token}"
        # In a real app, you'd store the CSRF token in the user's session
        # to validate it on callback.
        logger.info("Generated state for user %s: %s", user_id, state)
        
        return await client.get_oauth_url(state=state, redirect_uri=redirect_uri)

    async def finalize_connection(
        self, platform: str, request: Request, callback_query: connection_schemas.OAuthCallbackQuery
    ) -> SocialConnection:
        """
        Handles the callback from the social platform, exchanges the code for
        tokens, and saves the connection.
        """
        if callback_query.error:
            raise OAuthConnectionError(
                f"OAuth failed on platform '{platform}': {callback_query.error} - "
                f"{callback_query.error_description}"
            )
        
        if not callback_query.code or not callback_query.state:
            raise OAuthConnectionError("Invalid callback: code or state is missing.")
            
        try:
            user_id, csrf_token = callback_query.state.split(":", 1)
            # Here you would validate csrf_token against the user's session
        except (ValueError, IndexError):
            raise OAuthConnectionError("Invalid state parameter received.")

        client = self._get_platform_client(platform)
        redirect_uri = str(
            request.url_for(
                "handle_oauth_callback_connect__platform__callback_get",
                platform=platform,
            )
        )

        token_data = await client.exchange_code_for_token(callback_query.code, redirect_uri)
        profile_data = await client.get_user_profile(token_data["access_token"])

        try:
            encrypted_access_token = self.encryption_service.encrypt_token(
                token_data["access_token"]
            )
            encrypted_refresh_token = (
                self.encryption_service.encrypt_token(token_data["refresh_token"])
                if token_data.get("refresh_token")
                else None
            )
        except Exception as e:
            raise TokenEncryptionError("Failed to encrypt tokens.") from e

        expires_at = (
            datetime.now(timezone.utc) + timedelta(seconds=token_data["expires_in"])
            if token_data.get("expires_in")
            else None
        )

        connection = await self.repo.get_by_user_and_platform(user_id, platform)
        if connection:
            logger.info("Updating existing connection for user %s, platform %s", user_id, platform)
            connection.external_user_id = profile_data["id"]
            connection.external_display_name = profile_data.get("display_name")
            connection.access_token_encrypted = encrypted_access_token
            connection.refresh_token_encrypted = encrypted_refresh_token
            connection.expires_at = expires_at
            connection.scopes = token_data.get("scope", "").split()
            connection.updated_at = datetime.now(timezone.utc)
        else:
            logger.info("Creating new connection for user %s, platform %s", user_id, platform)
            connection = SocialConnection(
                id=uuid4(),
                user_id=user_id,
                platform=platform,
                external_user_id=profile_data["id"],
                external_display_name=profile_data.get("display_name"),
                access_token_encrypted=encrypted_access_token,
                refresh_token_encrypted=encrypted_refresh_token,
                expires_at=expires_at,
                scopes=token_data.get("scope", "").split(),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
        
        return await self.repo.save(connection)

    async def get_user_connections(self, user_id: str) -> list[SocialConnection]:
        return await self.repo.list_by_user_id(user_id)

    async def disconnect(self, connection_id: str, user_id: str):
        connection = await self.repo.get_by_id(connection_id)
        if not connection:
            raise ConnectionNotFoundError(f"Connection with ID '{connection_id}' not found.")
        if connection.user_id != user_id:
            raise PermissionDeniedError("User does not own this connection.")

        client = self._get_platform_client(connection.platform)
        try:
            access_token = self.encryption_service.decrypt_token(connection.access_token_encrypted)
            await client.revoke_token(access_token)
            logger.info("Successfully revoked token for connection %s on platform %s", connection_id, connection.platform)
        except Exception as e:
            logger.warning(
                "Could not revoke token for connection %s on platform %s. It might be expired or invalid. Proceeding with deletion. Error: %s",
                connection_id,
                connection.platform,
                e,
            )

        await self.repo.delete(connection_id)
        logger.info("Deleted connection %s from database.", connection_id)

    async def get_valid_access_token(self, connection_id: str, user_id: str) -> str:
        connection = await self.repo.get_by_id(connection_id)
        if not connection:
            raise ConnectionNotFoundError(f"Connection with ID '{connection_id}' not found.")
        if connection.user_id != user_id:
            raise PermissionDeniedError("User does not own this connection.")

        if not connection.is_token_expired():
            return self.encryption_service.decrypt_token(connection.access_token_encrypted)
        
        if not connection.refresh_token_encrypted:
            raise TokenExpiredError("Token is expired and no refresh token is available.")

        logger.info("Access token for connection %s is expired. Attempting refresh.", connection_id)
        client = self._get_platform_client(connection.platform)
        decrypted_refresh_token = self.encryption_service.decrypt_token(connection.refresh_token_encrypted)
        
        try:
            new_token_data = await client.refresh_access_token(decrypted_refresh_token)
            
            new_access_token = new_token_data["access_token"]
            new_expires_in = new_token_data["expires_in"]
            new_expires_at = datetime.now(timezone.utc) + timedelta(seconds=new_expires_in)

            connection.update_tokens(
                new_access_token_encrypted=self.encryption_service.encrypt_token(new_access_token),
                new_expires_at=new_expires_at,
            )
            await self.repo.save(connection)
            logger.info("Successfully refreshed and saved token for connection %s.", connection_id)
            return new_access_token

        except Exception as e:
            logger.error("Failed to refresh token for connection %s: %s", connection_id, e, exc_info=True)
            raise TokenExpiredError(f"Failed to refresh token for connection {connection_id}. Re-authentication may be required.") from e