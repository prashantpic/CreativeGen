# -*- coding: utf-8 -*-
"""
HTTP client for interacting with an internal Asset Management Service.
"""
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional
from uuid import UUID

import httpx

from core.config import Settings
from core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class AssetManagementClient:
    """Client for communicating with an internal Asset Management Service."""

    def __init__(self, base_url: str, timeout: int = 10):
        """
        Initializes the AssetManagementClient.

        :param base_url: The base URL of the Asset Management service.
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
            logger.info("AssetManagementClient closed.")

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
                "HTTP error calling Asset Management Service at %s: %s - %s",
                e.request.url,
                e.response.status_code,
                e.response.text,
                exc_info=True,
            )
            raise ExternalServiceError(
                detail=f"Error with Asset Management Service: {e.response.status_code}",
                status_code=e.response.status_code,
            )
        except httpx.RequestError as e:
            logger.error(
                "Request error calling Asset Management Service at %s: %s",
                e.request.url,
                e,
                exc_info=True,
            )
            raise ExternalServiceError(
                detail="Could not connect to Asset Management Service."
            )

    async def get_asset_details(
        self, asset_id: UUID, internal_auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends a request to get the details of an existing asset.

        :param asset_id: The UUID of the asset to query.
        :param internal_auth_token: An internal service-to-service auth token, if required.
        :return: A dictionary representing the asset details response.
        """
        headers = {}
        if internal_auth_token:
            headers["Authorization"] = f"Bearer {internal_auth_token}"

        response = await self._request("GET", f"/assets/{asset_id}", headers=headers)
        return response.json()

    # Placeholder for more complex operations like uploads
    async def upload_asset_proxy(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Placeholder for proxying an asset upload request.
        This would involve handling multipart/form-data and streaming the request body.
        """
        logger.warning("upload_asset_proxy is a placeholder and not implemented.")
        # Example of how it might look:
        # headers = kwargs.get("headers", {})
        # files = kwargs.get("files")
        # data = kwargs.get("data")
        # response = await self._request("POST", "/assets", headers=headers, files=files, data=data)
        # return response.json()
        raise NotImplementedError("Asset upload proxy functionality is not implemented.")


# Singleton instance and dependency provider
_asset_management_client: Optional[AssetManagementClient] = None


@asynccontextmanager
async def asset_management_client_lifespan(
    settings: Settings,
) -> AsyncGenerator[AssetManagementClient, None]:
    """Manages the AssetManagementClient lifecycle."""
    global _asset_management_client
    _asset_management_client = AssetManagementClient(
        base_url=settings.ASSET_MANAGEMENT_SERVICE_URL
    )
    logger.info("AssetManagementClient initialized.")
    yield _asset_management_client
    await _asset_management_client.close()
    _asset_management_client = None


def get_asset_management_client() -> AssetManagementClient:
    """FastAPI dependency to get the AssetManagementClient instance."""
    if _asset_management_client is None:
        raise RuntimeError("AssetManagementClient not initialized.")
    return _asset_management_client