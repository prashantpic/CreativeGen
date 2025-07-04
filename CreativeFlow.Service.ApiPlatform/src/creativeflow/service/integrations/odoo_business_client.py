import logging
import uuid
from typing import Any, Dict

import httpx
from fastapi import HTTPException, status

from creativeflow.service.core.config import settings

logger = logging.getLogger(__name__)


class OdooBusinessClient:
    """
    HTTP client for communicating with the internal Odoo Business Service.

    This client encapsulates the API calls for checking user quotas and logging
    API usage, handling HTTP requests, and basic error management.
    """

    def __init__(self):
        """Initializes the asynchronous HTTP client."""
        # Using a context-managed client is preferred for production apps
        # to handle connection pooling and lifecycle correctly.
        # For simplicity in dependency injection, we create it here.
        # In a more complex scenario, this could be managed by the application lifespan.
        self.client = httpx.AsyncClient(
            base_url=str(settings.ODOO_BUSINESS_SERVICE_URL),
            timeout=10.0,
            # In a real system, you'd have a secure way to authenticate services
            # e.g., using a bearer token or mTLS.
            # headers={"Authorization": f"Bearer {settings.INTERNAL_SERVICE_TOKEN}"}
        )

    async def check_user_quota(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Sends a request to the Odoo service to get quota/credit info for a given user.

        Args:
            user_id: The UUID of the user whose quota needs to be checked.

        Returns:
            A dictionary containing quota information. Expected to have keys like
            'can_transact' (bool) and 'message' (str).

        Raises:
            HTTPException: If the service call fails or returns an error.
        """
        try:
            response = await self.client.get(f"/internal/api/v1/quota/{user_id}")
            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx responses
            return response.json()
        except httpx.RequestError as exc:
            logger.error(f"Request to Odoo quota check failed for user {user_id}: {exc}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="The business service is currently unreachable.",
            )
        except httpx.HTTPStatusError as exc:
            logger.error(f"Odoo quota check returned error for user {user_id}: {exc.response.status_code} {exc.response.text}")
            # Forward the status code and detail if possible, otherwise use a generic error
            detail = exc.response.json().get("detail", "An error occurred with the business service.")
            raise HTTPException(status_code=exc.response.status_code, detail=detail)

    async def log_api_usage(self, user_id: uuid.UUID, usage_details: Dict[str, Any]):
        """
        Sends a request to log API usage and deduct credits.

        Args:
            user_id: The UUID of the user to log usage for.
            usage_details: A dictionary with details of the API call (e.g., cost, type).

        Raises:
            HTTPException: If the service call fails.
        """
        payload = {"user_id": str(user_id), "details": usage_details}
        try:
            response = await self.client.post("/internal/api/v1/usage/log", json=payload)
            response.raise_for_status()
            logger.info(f"Successfully logged API usage for user {user_id} via Odoo service.")
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error(f"Failed to log API usage for user {user_id} in Odoo: {exc}")
            # This is a critical issue that should be flagged for monitoring/alerting.
            # We don't raise an HTTPException here as the user's request has already
            # been processed. This failure needs to be handled by a reconciliation process.
            pass