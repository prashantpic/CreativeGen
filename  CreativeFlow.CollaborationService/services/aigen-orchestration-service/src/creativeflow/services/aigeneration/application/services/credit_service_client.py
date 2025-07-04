import logging
from uuid import UUID
import httpx
from fastapi import status

logger = logging.getLogger(__name__)

# Custom Exceptions
class CreditServiceError(Exception):
    """Base exception for Credit Service client errors."""
    pass

class InsufficientCreditsError(CreditServiceError):
    """Raised when a user has insufficient credits for an action."""
    pass


class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """
    def __init__(self, base_url: str):
        self._base_url = base_url
        # For production, this client should be managed as a singleton
        # and initialized/closed at app startup/shutdown.
        self._http_client = httpx.AsyncClient(base_url=self._base_url, timeout=10.0)

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Internal request helper."""
        try:
            response = await self._http_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(f"Credit Service HTTP error: {e.response.status_code} for {e.request.url} - {e.response.text}")
            if e.response.status_code == status.HTTP_402_PAYMENT_REQUIRED:
                raise InsufficientCreditsError(e.response.json().get("detail", "Insufficient credits.")) from e
            raise CreditServiceError(f"Credit Service returned status {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error(f"Credit Service request error: {e.request.url} - {e}")
            raise CreditServiceError(f"Could not connect to Credit Service: {e}") from e

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has enough credits.
        This is illustrative; a real implementation might be a single deduct call
        that atomically checks and deducts.
        """
        logger.info(f"Checking credits for user_id: {user_id}, required: {required_credits}")
        response = await self._request("GET", f"/users/{user_id}/credits")
        balance = response.json().get("balance", 0.0)
        if balance < required_credits:
            raise InsufficientCreditsError(f"User {user_id} has {balance} credits, but {required_credits} are required.")
        return True

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """Deducts a specified amount of credits from a user's account."""
        logger.info(f"Deducting {amount} credits from user_id: {user_id} for action: {action_type}, request_id: {request_id}")
        payload = {
            "amount": amount,
            "action_type": action_type,
            "reference_id": str(request_id)
        }
        response = await self._request("POST", f"/users/{user_id}/credits/deduct", json=payload)
        return response.json().get("success", False)

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """Refunds a specified amount of credits to a user's account."""
        logger.info(f"Refunding {amount} credits to user_id: {user_id} for request_id: {request_id}. Reason: {reason}")
        payload = {
            "amount": amount,
            "reason": reason,
            "reference_id": str(request_id)
        }
        response = await self._request("POST", f"/users/{user_id}/credits/refund", json=payload)
        return response.json().get("success", False)

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """Retrieves the subscription tier for a given user."""
        logger.info(f"Getting subscription tier for user_id: {user_id}")
        response = await self._request("GET", f"/users/{user_id}/subscription")
        return response.json().get("tier", "Free")

    async def close(self):
        """Closes the underlying httpx client."""
        await self._http_client.aclose()