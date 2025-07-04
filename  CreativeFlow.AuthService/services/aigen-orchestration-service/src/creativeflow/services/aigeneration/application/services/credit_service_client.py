import logging
from uuid import UUID
import httpx
from pydantic import AnyUrl

from .orchestration_service import InsufficientCreditsError

logger = logging.getLogger(__name__)

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """
    def __init__(self, base_url: AnyUrl, http_client: httpx.AsyncClient):
        self._base_url = str(base_url)
        self._http_client = http_client

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Helper method to make HTTP requests."""
        url = f"{self._base_url}{endpoint}"
        try:
            response = await self._http_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Credit Service request failed: {e.request.method} {e.request.url} - Status {e.response.status_code} - "
                f"Response: {e.response.text}"
            )
            if e.response.status_code == 402:
                raise InsufficientCreditsError(user_id="unknown", detail=f"Credit service error: {e.response.json().get('detail', 'Payment Required')}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Credit Service connection error: {e.request.method} {e.request.url} - {e}")
            raise

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has enough credits.
        Raises InsufficientCreditsError if the user does not have enough credits.
        Returns True if credits are sufficient.
        """
        logger.info(f"Checking {required_credits} credits for user {user_id}")
        response = await self._request(
            "POST",
            f"/users/{user_id}/credits/check",
            json={"required_credits": required_credits}
        )
        return response.json().get("sufficient", False)

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """
        Deducts credits from a user's account.
        Raises InsufficientCreditsError if deduction fails due to lack of funds.
        Returns True on successful deduction.
        """
        logger.info(f"Deducting {amount} credits from user {user_id} for action '{action_type}' (request: {request_id})")
        payload = {
            "amount": amount,
            "action_type": action_type,
            "reference_id": str(request_id),
            "description": f"Credit deduction for AI generation action: {action_type}"
        }
        response = await self._request("POST", f"/users/{user_id}/credits/deduct", json=payload)
        return response.json().get("success", False)

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """

        Refunds credits to a user's account.
        Returns True on successful refund.
        """
        logger.info(f"Refunding {amount} credits to user {user_id} for request {request_id}. Reason: {reason}")
        payload = {
            "amount": amount,
            "reference_id": str(request_id),
            "reason": reason
        }
        response = await self._request("POST", f"/users/{user_id}/credits/refund", json=payload)
        return response.json().get("success", False)

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """
        Gets the subscription tier for a given user.
        """
        logger.info(f"Getting subscription tier for user {user_id}")
        response = await self._request("GET", f"/users/{user_id}/subscription")
        return response.json().get("tier", "Free")