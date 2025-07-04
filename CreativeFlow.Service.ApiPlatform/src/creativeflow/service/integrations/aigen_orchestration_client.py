import logging
import uuid
from typing import Any, Dict

import httpx
from fastapi import HTTPException, status

from creativeflow.service.core.config import settings
from creativeflow.service.api.v1.schemas.generation_schemas import GenerationRequestSchema

logger = logging.getLogger(__name__)


class AIGenOrchClient:
    """
    HTTP client for communicating with the AI Generation Orchestration Service.

    Encapsulates API calls for initiating and checking the status of generation jobs.
    It should implement resilience patterns like retries for transient errors.
    """

    def __init__(self):
        """Initializes the asynchronous HTTP client."""
        # A more robust implementation would use a transport with retries.
        # For example, using the `tenacity` library or httpx's built-in transport capabilities.
        self.client = httpx.AsyncClient(
            base_url=str(settings.AIGEN_ORCH_SERVICE_URL),
            timeout=30.0,
            headers={
                # Example of service-to-service authentication
                # "X-Internal-Service-Key": settings.AIGEN_INTERNAL_KEY
            }
        )

    async def initiate_generation(
        self,
        request_data: GenerationRequestSchema,
        user_id: uuid.UUID,
        api_client_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Sends a POST request to the orchestration service to start a generation job.

        Args:
            request_data: The Pydantic schema containing the user's request parameters.
            user_id: The ID of the user initiating the request.
            api_client_id: The ID of the APIClient used for the request.

        Returns:
            A dictionary containing the response from the orchestration service,
            expected to include a `job_id`.

        Raises:
            HTTPException: If the orchestration service is unavailable or returns an error.
        """
        payload = request_data.model_dump()
        # Add context for the orchestration service
        payload["context"] = {
            "user_id": str(user_id),
            "source": "api_platform",
            "api_client_id": str(api_client_id)
        }

        try:
            response = await self.client.post("/v1/jobs", json=payload)
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error(f"Failed to communicate with AI Generation Orchestration service: {exc}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI generation service is currently unavailable.",
            )

    async def get_generation_status(
        self,
        job_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any] | None:
        """
        Sends a GET request to retrieve the status of a specific generation job.

        Args:
            job_id: The ID of the job to check.
            user_id: The ID of the user requesting the status, for authorization checks.

        Returns:
            A dictionary with the job's status details, or None if not found.

        Raises:
            HTTPException: If the service is unavailable. A 404 is handled by returning None.
        """
        try:
            # Pass user_id as a query param for the orchestrator to authorize the request
            response = await self.client.get(f"/v1/jobs/{job_id}", params={"user_id": str(user_id)})
            
            if response.status_code == 404:
                return None
            
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            logger.error(f"Failed to get job status from AI Orchestration service: {exc}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI generation service is currently unavailable.",
            )
        except httpx.HTTPStatusError as exc:
            logger.error(f"AI Orchestration service returned error for job status: {exc.response.status_code}")
            detail = exc.response.json().get("detail", "An error occurred with the generation service.")
            raise HTTPException(status_code=exc.response.status_code, detail=detail)