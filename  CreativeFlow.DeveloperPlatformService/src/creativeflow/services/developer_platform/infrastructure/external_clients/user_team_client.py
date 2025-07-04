# -*- coding: utf-8 -*-
"""
HTTP client for interacting with an internal User/Team Management Service.
"""
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional
from uuid import UUID

import httpx

from core.config import Settings
from core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class UserTeamClient:
    """Client for communicating with an internal User/Team Management Service."""

    def __init__(self, base_url: str, timeout: int = 5):
        """
        Initializes the UserTeamClient.

        :param base_url: The base URL of the User/Team Management service.
        :param timeout: The request timeout in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Initializes and returns the httpx.AsyncClient instance."""
        if self._client is None or self._client.is_closed:
            # Placeholder for retry/circuit breaker logic
            self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self._client

    async def close(self):
        """Closes the httpx.AsyncClient."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
            logger.info("UserTeamClient closed.")

    async def _request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> httpx.Response:
        """
        Makes an asynchronous HTTP request to the external service.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param endpoint: The API endpoint path.
        :param kwargs: Additional arguments for the httpx request.
        :raises ExternalServiceError: If the request fails or returns an error status.
        :return: The httpx.Response object.
        """
        client = await self._get_client()
        try:
            response = await client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP error calling User/Team Service at %s: %s - %s",
                e.request.url,
                e.response.status_code,
                e.response.text,
                exc_info=True,
            )
            raise ExternalServiceError(
                detail=f"Error with User/Team Service: {e.response.status_code}",
                status_code=e.response.status_code,
            )
        except httpx.RequestError as e:
            logger.error(
                "Request error calling User/Team Service at %s: %s",
                e.request.url,
                e,
                exc_info=True,
            )
            raise ExternalServiceError(detail="Could not connect to User/Team Service.")

    async def get_user_details(
        self, user_id: UUID, internal_auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends a request to get the details of a user.

        :param user_id: The UUID of the user to query.
        :param internal_auth_token: An internal service-to-service auth token.
        :return: A dictionary representing the user details response.
        """
        headers = {}
        if internal_auth_token:
            headers["Authorization"] = f"Bearer {internal_auth_token}"

        response = await self._request("GET", f"/users/{user_id}", headers=headers)
        return response.json()

    async def get_team_details(
        self, team_id: UUID, internal_auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends a request to get the details of a team.

        :param team_id: The UUID of the team to query.
        :param internal_auth_token: An internal service-to-service auth token.
        :return: A dictionary representing the team details response.
        """
        headers = {}
        if internal_auth_token:
            headers["Authorization"] = f"Bearer {internal_auth_token}"

        response = await self._request("GET", f"/teams/{team_id}", headers=headers)
        return response.json()


# Singleton instance and dependency provider
_user_team_client: Optional[UserTeamClient] = None


@asynccontextmanager
async def user_team_client_lifespan(
    settings: Settings,
) -> AsyncGenerator[UserTeamClient, None]:
    """Manages the UserTeamClient lifecycle."""
    global _user_team_client
    _user_team_client = UserTeamClient(base_url=settings.USER_TEAM_SERVICE_URL)
    logger.info("UserTeamClient initialized.")
    yield _user_team_client
    await _user_team_client.close()
    _user_team_client = None


def get_user_team_client() -> UserTeamClient:
    """FastAPI dependency to get the UserTeamClient instance."""
    if _user_team_client is None:
        raise RuntimeError("UserTeamClient not initialized.")
    return _user_team_client