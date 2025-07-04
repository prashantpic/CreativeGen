import logging
from uuid import UUID
import httpx
from fastapi import status

from creativeflow.services.aigeneration.core.error_handlers import InsufficientCreditsError, CreditServiceError

logger = logging.getLogger(__name__)

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url
        self._http_client = http_client

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Helper method to make requests and handle common errors."""
        url = f"{self._base_url}{endpoint}"
        try:
            response = await self._http_client.request(method, url, timeout=10.0, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Credit Service returned an error: {e.response.status_code} "
                f"for {method} {url}. Response: {e.response.text}"
            )
            if e.response.status_code == status.HTTP_402_PAYMENT_REQUIRED:
                raise InsufficientCreditsError(e.response.json().get("detail", "Insufficient credits"))
            raise CreditServiceError(f"Credit Service failed with status {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Could not connect to Credit Service at {url}: {e}")
            raise CreditServiceError(f"Failed to connect to Credit Service: {e}")

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """Checks if a user has sufficient credits."""
        logger.info(f"Checking if user {user_id} has {required_credits} credits.")
        response = await self._request("POST", "/credits/check", json={
            "user_id": user_id,
            "required_credits": required_credits
        })
        return response.json().get("has_sufficient_credits", False)

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """Deducts a specified amount of credits from a user's account."""
        logger.info(f"Deducting {amount} credits from user {user_id} for action '{action_type}' (request: {request_id}).")
        response = await self._request("POST", "/credits/deduct", json={
            "user_id": user_id,
            "transaction_id": str(request_id), # Use generation request ID as unique transaction ID
            "amount": amount,
            "description": f"AI Generation: {action_type}"
        })
        return response.json().get("success", False)

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """Refunds a specified amount of credits to a user's account."""
        logger.info(f"Refunding {amount} credits to user {user_id} for request {request_id}. Reason: {reason}")
        response = await self._request("POST", "/credits/refund", json={
            "user_id": user_id,
            "original_transaction_id": str(request_id),
            "amount": amount,
            "reason": reason
        })
        return response.json().get("success", False)

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """Retrieves the subscription tier for a given user."""
        logger.info(f"Getting subscription tier for user {user_id}.")
        response = await self._request("GET", f"/subscriptions/user/{user_id}")
        return response.json().get("tier", "Free")