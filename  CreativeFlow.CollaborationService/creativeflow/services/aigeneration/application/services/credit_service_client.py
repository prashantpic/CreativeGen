import logging
from uuid import UUID

import httpx
from pydantic import AnyUrl

from creativeflow.services.aigeneration.application.exceptions import InsufficientCreditsError, CreditServiceError

logger = logging.getLogger(__name__)

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """

    def __init__(self, base_url: AnyUrl, http_client: httpx.AsyncClient):
        self._base_url = str(base_url)
        self._http_client = http_client

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has sufficient credits.
        Raises InsufficientCreditsError if the check fails.
        Raises CreditServiceError for other communication failures.
        """
        url = f"{self._base_url}/users/{user_id}/check"
        try:
            response = await self._http_client.post(url, json={"required_credits": required_credits})
            response.raise_for_status()
            
            # Assuming a successful response means they have enough credits
            logger.info("Credit check successful for user %s, required: %f", user_id, required_credits)
            return True

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 402:
                detail = e.response.json().get("detail", "Insufficient credits.")
                logger.warning("Insufficient credits for user %s: %s", user_id, detail)
                raise InsufficientCreditsError(detail) from e
            
            logger.error("Credit Service returned an error during credit check: %s", e)
            raise CreditServiceError(f"Credit service check failed with status {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error("Failed to connect to Credit Service during credit check: %s", e)
            raise CreditServiceError("Could not connect to the Credit Service.") from e


    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """
        Deducts a specified amount of credits from a user's account.
        Returns True on success. Raises CreditServiceError on failure.
        """
        url = f"{self._base_url}/users/{user_id}/deduct"
        payload = {
            "amount": amount,
            "action_type": action_type,
            "reference_id": str(request_id),
            "description": f"Credit deduction for {action_type} on request {request_id}"
        }
        try:
            response = await self._http_client.post(url, json=payload)
            response.raise_for_status()

            logger.info("Successfully deducted %f credits from user %s for action %s", amount, user_id, action_type)
            return True

        except httpx.HTTPStatusError as e:
            # Deduction might fail due to insufficient credits even after a check (race condition)
            if e.response.status_code == 402:
                 detail = e.response.json().get("detail", "Insufficient credits for deduction.")
                 logger.error("Credit deduction failed for user %s: %s", user_id, detail)
                 raise InsufficientCreditsError(detail) from e
            
            logger.error("Credit Service returned an error during credit deduction: %s", e)
            raise CreditServiceError(f"Credit service deduction failed with status {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error("Failed to connect to Credit Service during credit deduction: %s", e)
            raise CreditServiceError("Could not connect to the Credit Service.") from e


    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """

        Refunds a specified amount of credits to a user's account.
        Returns True on success. Raises CreditServiceError on failure.
        """
        url = f"{self._base_url}/users/{user_id}/refund"
        payload = {
            "amount": amount,
            "reference_id": str(request_id),
            "reason": reason
        }
        try:
            response = await self._http_client.post(url, json=payload)
            response.raise_for_status()

            logger.info("Successfully refunded %f credits to user %s. Reason: %s", amount, user_id, reason)
            return True

        except httpx.HTTPError as e:
            # We log the error but do not re-raise a fatal exception,
            # as the primary generation flow should not fail because a refund failed.
            # This should be monitored and handled by an external system.
            logger.error("Credit refund failed for user %s, request %s. Error: %s", user_id, request_id, e)
            return False


    async def get_user_subscription_tier(self, user_id: str) -> str:
        """
        Retrieves the subscription tier for a given user.
        Raises CreditServiceError on failure.
        """
        url = f"{self._base_url}/users/{user_id}/subscription"
        try:
            response = await self._http_client.get(url)
            response.raise_for_status()
            
            tier = response.json().get("tier", "Free")
            logger.debug("Fetched subscription tier for user %s: %s", user_id, tier)
            return tier

        except httpx.HTTPError as e:
            logger.error("Failed to get subscription tier for user %s. Error: %s", user_id, e)
            raise CreditServiceError("Could not retrieve user subscription tier.") from e