import logging
from uuid import UUID
from typing import Optional

import httpx
from fastapi import Depends
from functools import lru_cache

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.application.exceptions import (
    CreditServiceError,
    InsufficientCreditsError
)

logger = logging.getLogger(__name__)

class CreditServiceClient:
    """
    Client for interacting with the external Credit/Subscription Service API.
    """
    def __init__(self, base_url: str):
        self._http_client = httpx.AsyncClient(base_url=base_url, timeout=10.0)

    async def close(self):
        await self._http_client.aclose()

    async def check_credits(self, user_id: str, required_credits: float) -> bool:
        """Checks if a user has enough credits."""
        try:
            response = await self._http_client.post(
                "/credits/check",
                json={"user_id": user_id, "required_amount": required_credits}
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("has_sufficient_credits", False):
                raise InsufficientCreditsError(f"User {user_id} has insufficient credits. Required: {required_credits}.")
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 402:
                raise InsufficientCreditsError(f"User {user_id} has insufficient credits. Required: {required_credits}.")
            logger.error(f"Credit service error during check_credits for user {user_id}: {e.response.text}", exc_info=True)
            raise CreditServiceError(f"Failed to check credits: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"HTTP request error during check_credits for user {user_id}: {e}", exc_info=True)
            raise CreditServiceError(f"Credit service is unreachable.")

    async def deduct_credits(self, user_id: str, request_id: UUID, amount: float, action_type: str) -> bool:
        """Deducts credits from a user's account."""
        try:
            response = await self._http_client.post(
                "/credits/deduct",
                json={
                    "user_id": user_id,
                    "amount": amount,
                    "transaction_details": {
                        "source_service": "aigen_orchestration",
                        "generation_request_id": str(request_id),
                        "action_type": action_type
                    }
                }
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except httpx.HTTPStatusError as e:
            logger.error(f"Credit service error during deduct_credits for user {user_id}: {e.response.text}", exc_info=True)
            raise CreditServiceError(f"Failed to deduct credits: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"HTTP request error during deduct_credits for user {user_id}: {e}", exc_info=True)
            raise CreditServiceError(f"Credit service is unreachable.")

    async def refund_credits(self, user_id: str, request_id: UUID, amount: float, reason: str) -> bool:
        """Refunds credits to a user's account."""
        try:
            response = await self._http_client.post(
                "/credits/refund",
                json={
                    "user_id": user_id,
                    "amount": amount,
                    "transaction_details": {
                        "source_service": "aigen_orchestration",
                        "generation_request_id": str(request_id),
                        "reason": reason
                    }
                }
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except httpx.HTTPStatusError as e:
            logger.error(f"Credit service error during refund_credits for user {user_id}: {e.response.text}", exc_info=True)
            raise CreditServiceError(f"Failed to refund credits: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"HTTP request error during refund_credits for user {user_id}: {e}", exc_info=True)
            raise CreditServiceError(f"Credit service is unreachable.")

    async def get_user_subscription_tier(self, user_id: str) -> Optional[str]:
        """Gets the user's current subscription tier."""
        try:
            response = await self._http_client.get(f"/subscriptions/user/{user_id}/tier")
            response.raise_for_status()
            return response.json().get("tier")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"No subscription tier found for user {user_id}.")
                return None
            logger.error(f"Credit service error during get_user_subscription_tier for user {user_id}: {e.response.text}", exc_info=True)
            raise CreditServiceError(f"Failed to get subscription tier: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"HTTP request error during get_user_subscription_tier for user {user_id}: {e}", exc_info=True)
            raise CreditServiceError(f"Credit service is unreachable.")


@lru_cache()
def get_credit_service_client() -> CreditServiceClient:
    """
    Dependency to get a singleton instance of the CreditServiceClient.
    """
    return CreditServiceClient(base_url=str(settings.CREDIT_SERVICE_API_URL))