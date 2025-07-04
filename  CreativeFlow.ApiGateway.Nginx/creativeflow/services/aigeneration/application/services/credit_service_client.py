import logging
from uuid import UUID
import httpx

from ...core.error_handlers import InsufficientCreditsError, ExternalServiceError

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """
    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url
        self._http_client = http_client
        self.service_name = "Credit Service"

    async def _make_request(self, method: str, endpoint: str, **kwargs):
        """Helper method to make HTTP requests and handle common errors."""
        url = f"{self._base_url}{endpoint}"
        try:
            response = await self._http_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred while calling {self.service_name}: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 402:
                raise InsufficientCreditsError(detail=e.response.json().get("detail", "Insufficient credits."))
            raise ExternalServiceError(
                service_name=self.service_name,
                detail=f"Received status {e.response.status_code} from credit service."
            )
        except httpx.RequestError as e:
            logging.error(f"Request error occurred while calling {self.service_name}: {e}")
            raise ExternalServiceError(service_name=self.service_name, detail="Could not connect to credit service.")

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has enough credits.
        Returns True if credits are sufficient, otherwise raises InsufficientCreditsError.
        """
        logging.info(f"Checking {required_credits} credits for user {user_id}")
        # This endpoint is expected to return a 200 OK if credits are sufficient,
        # or a 402 Payment Required if they are not.
        await self._make_request(
            "POST",
            "/check",
            json={"user_id": user_id, "required_credits": required_credits}
        )
        logging.info(f"Credit check passed for user {user_id}")
        return True

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """
        Deducts a specific amount of credits for a given action.
        Returns True on success.
        """
        logging.info(f"Deducting {amount} credits from user {user_id} for action '{action_type}' (request: {request_id})")
        payload = {
            "user_id": user_id,
            "request_id": str(request_id),
            "amount": amount,
            "action_type": action_type
        }
        await self._make_request("POST", "/deduct", json=payload)
        logging.info(f"Successfully deducted {amount} credits from user {user_id}")
        return True

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """
        Refunds a specific amount of credits for a given request.
        Returns True on success.
        """
        logging.info(f"Refunding {amount} credits to user {user_id} for request {request_id}. Reason: {reason}")
        payload = {
            "user_id": user_id,
            "request_id": str(request_id),
            "amount": amount,
            "reason": reason
        }
        await self._make_request("POST", "/refund", json=payload)
        logging.info(f"Successfully refunded {amount} credits to user {user_id}")
        return True

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """
        Gets the user's current subscription tier.
        """
        logging.info(f"Fetching subscription tier for user {user_id}")
        response_data = await self._make_request("GET", f"/{user_id}/subscription")
        tier = response_data.get("tier", "Free")
        logging.info(f"User {user_id} is on tier: {tier}")
        return tier