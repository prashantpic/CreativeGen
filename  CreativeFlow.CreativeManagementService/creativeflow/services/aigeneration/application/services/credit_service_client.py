import logging
from uuid import UUID
import httpx

logger = logging.getLogger(__name__)

class InsufficientCreditsError(Exception):
    def __init__(self, user_id: str, required: float, has: float):
        self.user_id = user_id
        self.required = required
        self.has = has
        super().__init__(f"User {user_id} has insufficient credits. Required: {required}, Has: {has}.")

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """
    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url
        self._http_client = http_client

    async def _handle_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Helper to make requests and handle common errors."""
        try:
            url = f"{self._base_url}{endpoint}"
            response = await self._http_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(f"Credit Service returned error {e.response.status_code} for {e.request.url}: {e.response.text}")
            # Re-raise or handle specific status codes
            raise
        except httpx.RequestError as e:
            logger.error(f"Error connecting to Credit Service at {e.request.url}: {e}")
            raise

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has enough credits.
        Raises InsufficientCreditsError if they do not.
        """
        logger.info(f"Checking credits for user {user_id}. Required: {required_credits}")
        response = await self._handle_request("GET", f"/users/{user_id}/balance")
        balance = response.json().get("balance", 0.0)
        
        if balance < required_credits:
            raise InsufficientCreditsError(user_id=user_id, required=required_credits, has=balance)
        
        return True

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """Deducts credits from a user's account for a specific action."""
        logger.info(f"Deducting {amount} credits from user {user_id} for action '{action_type}' (request {request_id}).")
        payload = {
            "amount": amount,
            "action_type": action_type,
            "reference_id": str(request_id),
            "description": f"Credit deduction for {action_type}"
        }
        response = await self._handle_request("POST", f"/users/{user_id}/deduct", json=payload)
        return response.json().get("success", False)

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """Refunds credits to a user's account."""
        logger.info(f"Refunding {amount} credits to user {user_id} for request {request_id}. Reason: {reason}")
        payload = {
            "amount": amount,
            "reason": reason,
            "reference_id": str(request_id)
        }
        response = await self._handle_request("POST", f"/users/{user_id}/refund", json=payload)
        return response.json().get("success", False)

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """Gets the user's current subscription tier (e.g., 'Free', 'Pro')."""
        logger.debug(f"Getting subscription tier for user {user_id}")
        response = await self._handle_request("GET", f"/users/{user_id}/subscription")
        return response.json().get("tier", "Free")