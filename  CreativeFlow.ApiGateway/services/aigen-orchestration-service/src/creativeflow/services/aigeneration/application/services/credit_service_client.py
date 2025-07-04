import logging
from typing import Optional
from uuid import UUID

import httpx
from fastapi import status

logger = logging.getLogger(__name__)

# --- Custom Exceptions ---

class CreditServiceError(Exception):
    """Base exception for Credit Service client errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InsufficientCreditsError(CreditServiceError):
    """Raised when a user has insufficient credits for an action."""
    def __init__(self, user_id: str, required_credits: float, message: Optional[str] = None):
        self.user_id = user_id
        self.required_credits = required_credits
        super().__init__(
            message or f"User {user_id} has insufficient credits. Required: {required_credits}."
        )

# --- Client Implementation ---

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """
    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url
        self._http_client = http_client

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        try:
            url = f"{self._base_url}{endpoint}"
            response = await self._http_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_402_PAYMENT_REQUIRED:
                # Assuming the service returns a specific error for insufficient credits
                raise InsufficientCreditsError(
                    user_id=e.request.json().get("user_id", "unknown"),
                    required_credits=e.request.json().get("amount", 0),
                    message=e.response.json().get("detail", "Insufficient credits.")
                ) from e
            logger.error(f"Credit Service HTTP error: {e.response.status_code} - {e.response.text}")
            raise CreditServiceError(
                message=f"Credit Service returned status {e.response.status_code}",
                status_code=e.response.status_code
            ) from e
        except httpx.RequestError as e:
            logger.error(f"Could not connect to Credit Service: {e}")
            raise CreditServiceError(message=f"Error connecting to Credit Service: {e}") from e

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has enough credits.
        This is a conceptual method; the actual check might be part of deduct_credits.
        For this implementation, we assume a `POST /check` endpoint.
        """
        payload = {"user_id": user_id, "required_credits": required_credits}
        response = await self._request("POST", "/check", json=payload)
        return response.json().get("has_sufficient_credits", False)

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """
        Deducts credits from a user's account for a specific action.
        """
        payload = {
            "user_id": user_id,
            "request_id": str(request_id),
            "amount": amount,
            "action_type": action_type
        }
        logger.info(f"Deducting {amount} credits from user {user_id} for action '{action_type}'.")
        response = await self._request("POST", "/deduct", json=payload)
        return response.json().get("success", False)

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """
        Refunds credits to a user's account.
        """
        payload = {
            "user_id": user_id,
            "original_request_id": str(request_id),
            "amount": amount,
            "reason": reason
        }
        logger.info(f"Refunding {amount} credits to user {user_id} for reason: '{reason}'.")
        response = await self._request("POST", "/refund", json=payload)
        return response.json().get("success", False)

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """
        Retrieves the user's current subscription tier.
        """
        response = await self._request("GET", f"/{user_id}/subscription")
        # Example response: {"tier": "Pro"}
        return response.json().get("tier", "Free")