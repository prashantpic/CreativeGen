import logging
from uuid import UUID

import httpx
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

# Custom exceptions for the credit service client
class CreditServiceError(HTTPException):
    def __init__(self, detail: str = "An error occurred with the Credit Service."):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)

class InsufficientCreditsError(HTTPException):
    def __init__(self, detail: str = "Insufficient credits for the requested action."):
        super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail)


class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    This class encapsulates the communication details for all credit and subscription operations.
    """

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        """
        Initializes the CreditServiceClient.

        Args:
            base_url: The base URL of the Credit Service API.
            http_client: An instance of httpx.AsyncClient for making requests.
        """
        self._base_url = base_url.rstrip('/')
        self._http_client = http_client

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """
        Checks if a user has sufficient credits for an action.
        
        Raises:
            InsufficientCreditsError: If the user does not have enough credits.
            CreditServiceError: For any other API or network issue.
        Returns:
            True if credits are sufficient.
        """
        url = f"{self._base_url}/users/{user_id}/credits/check"
        try:
            response = await self._http_client.post(url, json={"required_credits": required_credits})
            
            if response.status_code == 402:
                raise InsufficientCreditsError(response.json().get("detail", "Insufficient credits."))
            
            response.raise_for_status() # Raises for 4xx/5xx responses not caught above
            
            result = response.json()
            if result.get("sufficient"):
                logger.info(f"Credit check successful for user {user_id} requiring {required_credits} credits.")
                return True
            else:
                # This case might be redundant if the API returns 402, but good for robustness
                raise InsufficientCreditsError(response.json().get("detail", "Insufficient credits."))

        except httpx.HTTPStatusError as e:
            logger.error(f"Credit service returned an error for user {user_id}: {e.response.text}")
            raise CreditServiceError(f"Credit service failed with status {e.response.status_code}.")
        except httpx.RequestError as e:
            logger.error(f"Could not connect to credit service at {e.request.url!r}.")
            raise CreditServiceError("Could not connect to the Credit Service.")

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """
        Deducts a specified amount of credits from a user's account.

        Returns:
            True if deduction was successful.
        Raises:
            CreditServiceError: If the deduction fails for any reason.
        """
        url = f"{self._base_url}/users/{user_id}/credits/deduct"
        payload = {
            "amount": amount,
            "action_type": action_type,
            "reference_id": str(request_id),
            "description": f"Deduction for {action_type} on request {request_id}"
        }
        try:
            response = await self._http_client.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Successfully deducted {amount} credits from user {user_id} for action '{action_type}'.")
            return response.json().get("success", False)
        except httpx.HTTPStatusError as e:
            logger.error(f"Credit deduction failed for user {user_id}. Status: {e.response.status_code}, Body: {e.response.text}")
            detail = e.response.json().get("detail", "Failed to deduct credits.")
            if e.response.status_code == 402:
                raise InsufficientCreditsError(detail)
            raise CreditServiceError(detail)
        except httpx.RequestError as e:
            logger.error(f"Could not connect to credit service for deduction: {e.request.url!r}.")
            raise CreditServiceError("Could not connect to the Credit Service for deduction.")

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """
        Refunds a specified amount of credits to a user's account.

        Returns:
            True if refund was successful.
        """
        url = f"{self._base_url}/users/{user_id}/credits/refund"
        payload = {
            "amount": amount,
            "reason": reason,
            "reference_id": str(request_id)
        }
        try:
            response = await self._http_client.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Successfully requested refund of {amount} credits for user {user_id}. Reason: '{reason}'.")
            return response.json().get("success", False)
        except httpx.HTTPStatusError as e:
            logger.error(f"Credit refund request failed for user {user_id}. Status: {e.response.status_code}, Body: {e.response.text}")
            # Do not raise an exception here, as refund failure should not stop the error handling flow.
            return False
        except httpx.RequestError as e:
            logger.error(f"Could not connect to credit service for refund: {e.request.url!r}.")
            return False

    async def get_user_subscription_tier(self, user_id: str) -> str:
        """
        Retrieves the subscription tier for a given user.

        Returns:
            The user's subscription tier as a string (e.g., "Free", "Pro").
        Raises:
            CreditServiceError: If the user or tier cannot be retrieved.
        """
        url = f"{self._base_url}/users/{user_id}/subscription"
        try:
            response = await self._http_client.get(url)
            response.raise_for_status()
            tier = response.json().get("tier", "Free")
            logger.debug(f"Retrieved subscription tier '{tier}' for user {user_id}.")
            return tier
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to get subscription tier for user {user_id}: {e.response.text}")
            raise CreditServiceError(f"Failed to retrieve user subscription tier (status: {e.response.status_code}).")
        except httpx.RequestError as e:
            logger.error(f"Could not connect to credit service for subscription check: {e.request.url!r}.")
            raise CreditServiceError("Could not connect to the Credit Service for subscription check.")