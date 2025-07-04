# -*- coding: utf-8 -*-
"""
HTTP client for interacting with the AI Generation Orchestration Service.
"""
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional, Tuple
from uuid import UUID

import httpx
from fastapi import Depends

from core.config import Settings, get_settings
from core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class AIGenerationClient:
    """Client for communicating with the AI Generation Orchestration Service."""

    def __init__(self, base_url: str, timeout: int = 15):
        """
        Initializes the AIGenerationClient.

        :param base_url: The base URL of the AI Generation Orchestration service.
        :param timeout: The request timeout in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Initializes and returns the httpx.AsyncClient instance."""
        if self._client is None or self._client.is_closed:
            # In a real-world scenario, you might add retry logic and circuit breakers here.
            # Example using tenacity (not included as a dependency in this example):
            # from tenacity import retry, stop_after_attempt, wait_fixed
            # self._request = retry(stop=stop_after_attempt(3), wait=wait_fixed(2))(self._request)
            self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self._client

    async def close(self):
        """Closes the httpx.AsyncClient."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
            logger.info("AIGenerationClient closed.")

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
                "HTTP error calling AI Generation Service at %s: %s - %s",
                e.request.url,
                e.response.status_code,
                e.response.text,
                exc_info=True,
            )
            raise ExternalServiceError(
                detail=f"Error with AI Generation Service: {e.response.status_code}",
                status_code=e.response.status_code,
            )
        except httpx.RequestError as e:
            logger.error(
                "Request error calling AI Generation Service at %s: %s",
                e.request.url,
                e,
                exc_info=True,
            )
            raise ExternalServiceError(
                detail="Could not connect to AI Generation Service."
            )

    async def initiate_generation(
        self, payload: Dict[str, Any], internal_auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends a request to initiate a new creative generation.

        :param payload: The request payload, mirroring GenerationCreateRequestSchema.
        :param internal_auth_token: An internal service-to-service auth token, if required.
        :return: A dictionary representing the generation status response.
        """
        headers = {}
        if internal_auth_token:
            headers["Authorization"] = f"Bearer {internal_auth_token}"

        response = await self._request(
            "POST", "/generations", json=payload, headers=headers
        )
        return response.json()

    async def get_generation_status(
        self, generation_id: UUID, internal_auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends a request to get the status of an existing generation.

        :param generation_id: The UUID of the generation to query.
        :param internal_auth_token: An internal service-to-service auth token, if required.
        :return: A dictionary representing the generation status response.
        """
        headers = {}
        if internal_auth_token:
            headers["Authorization"] = f"Bearer {internal_auth_token}"

        response = await self._request(
            "GET", f"/generations/{generation_id}", headers=headers
        )
        return response.json()


# Singleton instance and dependency provider
_ai_generation_client: Optional[AIGenerationClient] = None


@asynccontextmanager
async def ai_generation_client_lifespan(
    settings: Settings,
) -> AsyncGenerator[AIGenerationClient, None]:
    """Manages the AIGenerationClient lifecycle."""
    global _ai_generation_client
    _ai_generation_client = AIGenerationClient(
        base_url=settings.AI_GENERATION_SERVICE_URL
    )
    logger.info("AIGenerationClient initialized.")
    yield _ai_generation_client
    await _ai_generation_client.close()
    _ai_generation_client = None


def get_ai_generation_client() -> AIGenerationClient:
    """FastAPI dependency to get the AIGenerationClient instance."""
    if _ai_generation_client is None:
        raise RuntimeError("AIGenerationClient not initialized.")
    return _ai_generation_client