import logging
import httpx
from uuid import UUID
from typing import Optional

logger = logging.getLogger(__name__)

# --- Custom Exceptions for the Credit Service Client ---

class CreditServiceError(Exception):
    """Base exception for credit service client errors."""
    def __init__(self, message="An error occurred with the Credit Service."):
        self.message = message
        super().__init__(self.message)

class InsufficientCreditsError(CreditServiceError):
    """Raised when a user has insufficient credits for an action."""
    def __init__(self, user_id: str, required: float, available: Optional[float] = None):
        message = f"User '{user_id}' has insufficient credits. Required: {required}"
        if available is not None:
            message += f", Available: {available}"
        super().__init__(message)

class CreditServiceUnavailableError(CreditServiceError):
    """Raised when the credit service cannot be reached."""
    def __init__(self, details: str):
        message = f"Credit Service is unavailable. Details: {details}"
        super().__init__(message)


class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """

    def __init__(self, http_client: httpx.AsyncClient, base_url: str):
        self._http_client = http_client
        self._base_url = base_url

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Helper method to make HTTP requests and handle common errors."""
        url = f"{self._base_url}{endpoint}"
        try:
            response = await self._http_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 402:
                data = e.response.json()
                raise InsufficientCreditsError(
                    user_id=data.get("user_id", "unknown"),
                    required=data.get("required", 0),
                    available=data.get("available")
                )
            logger.error(f"HTTP error calling Credit Service at {url}: {e.response.status_code} - {e.response.text}")
            raise CreditServiceError(f"Credit Service returned status {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Could not connect to Credit Service at {url}: {e}")
            raise CreditServiceUnavailableError(str(e))

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """Checks if a user has enough credits."""
        logger.info(f"Checking credits for user {user_id}. Required: {required_credits}")
        response = await self._make_request(
            "POST",
            "/check",
            json={"user_id": user_id, "required_credits": required_credits}
        )
        return response.json().get("has_sufficient_credits", False)

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """Deducts credits from a user's account for a specific action."""
        logger.info(f"Deducting {amount} credits from user {user_id} for action '{action_type}' (request: {request_id})")
        payload = {
            "user_id": user_id,
            "request_id": str(request_id),
            "amount": amount,
            "action_type": action_type
        }
        response = await self._make_request("POST", "/deduct", json=payload)
        return response.json().get("success", False)

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """Refunds credits to a user's account."""
        logger.info(f"Refunding {amount} credits to user {user_id} for request {request_id}. Reason: {reason}")
        payload = {
            "user_id": user_id,
            "request_id": str(request_id),
            "amount": amount,
            "reason": reason
        }
        response = await self._make_request("POST", "/refund", json=payload)
        return response.json().get("success", False)
        
    async def get_user_subscription_tier(self, user_id: str) -> str:
        """Gets the user's current subscription tier."""
        logger.info(f"Getting subscription tier for user {user_id}")
        response = await self._make_request("GET", f"/subscription/{user_id}")
        return response.json().get("tier", "Free")