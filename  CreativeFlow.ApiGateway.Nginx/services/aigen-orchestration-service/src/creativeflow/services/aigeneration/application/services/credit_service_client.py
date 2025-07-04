import httpx
import logging
from uuid import UUID
from fastapi import status

from creativeflow.services.aigeneration.core.error_handlers import InsufficientCreditsError, CreditDeductionError

logger = logging.getLogger(__name__)

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """
    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url.rstrip('/')
        self._http_client = http_client

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Helper method to make requests to the credit service."""
        url = f"{self._base_url}{endpoint}"
        try:
            response = await self._http_client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            # Log the detailed error from the downstream service
            response_text = e.response.text
            logger.error(
                f"Credit Service returned an error: {e.response.status_code} "
                f"for {method} {url}. Response: {response_text}"
            )
            # Re-raise with a more specific exception if possible
            if e.response.status_code == status.HTTP_402_PAYMENT_REQUIRED:
                 detail = e.response.json().get("detail", "Insufficient credits.")
                 raise InsufficientCreditsError(detail) from e
            raise CreditDeductionError(f"Credit Service failed with status {e.response.status_code}.") from e
        except httpx.RequestError as e:
            logger.error(f"Could not connect to Credit Service at {url}: {e}")
            raise CreditDeductionError(f"Could not connect to the Credit Service.") from e

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has enough credits.
        Raises InsufficientCreditsError if they do not.
        Returns True if they do.
        """
        logger.info(f"Checking if user {user_id} has {required_credits} credits.")
        # This endpoint is expected to return 200 OK if sufficient, and 402 if not.
        # The _request helper will handle the 402 and raise the correct exception.
        await self._request(
            "POST", 
            "/check-credits", 
            json={"user_id": user_id, "required_credits": required_credits}
        )
        logger.info(f"User {user_id} has sufficient credits.")
        return True

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """
        Deducts a specific amount of credits for a user for a given action.
        Raises CreditDeductionError on failure.
        Returns True on success.
        """
        logger.info(f"Deducting {amount} credits from user {user_id} for action '{action_type}' (request {request_id}).")
        await self._request(
            "POST",
            "/deduct-credits",
            json={
                "user_id": user_id,
                "request_id": str(request_id),
                "amount": amount,
                "action_type": action_type
            }
        )
        logger.info(f"Successfully deducted {amount} credits from user {user_id}.")
        return True

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """

        Refunds a specific amount of credits to a user.
        Logs errors but does not raise exceptions to avoid breaking the error handling flow.
        Returns True on success, False on failure.
        """
        logger.info(f"Attempting to refund {amount} credits to user {user_id} for request {request_id}. Reason: {reason}")
        try:
            await self._request(
                "POST",
                "/refund-credits",
                json={
                    "user_id": user_id,
                    "request_id": str(request_id),
                    "amount": amount,
                    "reason": reason
                }
            )
            logger.info(f"Successfully refunded {amount} credits to user {user_id}.")
            return True
        except Exception as e:
            # In refund scenarios, we log the error but don't want to fail the entire process.
            logger.error(f"Failed to refund credits for user {user_id}, request {request_id}: {e}")
            return False

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """
        Retrieves the subscription tier for a user.
        Raises CreditDeductionError if the user cannot be found or another error occurs.
        """
        logger.debug(f"Getting subscription tier for user {user_id}.")
        response = await self._request("GET", f"/users/{user_id}/subscription")
        tier = response.json().get("tier", "Unknown")
        logger.debug(f"User {user_id} subscription tier is '{tier}'.")
        return tier