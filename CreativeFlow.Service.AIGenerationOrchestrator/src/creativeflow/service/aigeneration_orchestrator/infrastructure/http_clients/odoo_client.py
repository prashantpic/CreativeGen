"""
Concrete implementation for communicating with the Odoo/CoreBusiness service.
Implements interfaces for checking credits, subscription status, and triggering
credit deductions.
"""
import logging
from decimal import Decimal
from uuid import UUID

import httpx

from ...app.interfaces import ICreditService

logger = logging.getLogger(__name__)


class OdooCreditService(ICreditService):
    """
    Implements an HTTP client to interact with the Odoo service for credit
    and subscription management.
    """

    def __init__(self, http_client: httpx.AsyncClient, odoo_service_url: str):
        self._http_client = http_client
        self._base_url = odoo_service_url

    async def check_and_reserve_credits(self, user_id: UUID, amount: Decimal) -> bool:
        """Makes an async POST request to the Odoo service to reserve credits."""
        url = f"{self._base_url}/api/v1/credits/check_and_reserve"
        payload = {"user_id": str(user_id), "amount": str(amount)}
        try:
            response = await self._http_client.post(url, json=payload, timeout=5.0)
            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx responses
            return response.json().get("can_afford", False)
        except httpx.HTTPStatusError as e:
            logger.error(f"Credit reservation failed for user {user_id}: HTTP {e.response.status_code} - {e.response.text}")
            return False
        except httpx.RequestError as e:
            logger.error(f"Credit reservation failed for user {user_id}: Request failed - {e}")
            return False

    async def deduct_credits(self, user_id: UUID, generation_id: UUID, amount: Decimal) -> None:
        """Makes an async POST request to the Odoo service to deduct credits."""
        url = f"{self._base_url}/api/v1/credits/deduct"
        payload = {"user_id": str(user_id), "generation_id": str(generation_id), "amount": str(amount)}
        try:
            response = await self._http_client.post(url, json=payload, timeout=5.0)
            response.raise_for_status()
            logger.info(f"Successfully deducted {amount} credits for user {user_id} and generation {generation_id}")
        except httpx.RequestError as e:
            logger.critical(f"Credit deduction failed for user {user_id}: {e}", exc_info=True)
            # This is a critical failure. Consider raising an exception to be handled upstream.
            raise

    async def refund_credits(self, user_id: UUID, generation_id: UUID, amount: Decimal) -> None:
        """Makes an async POST request to the Odoo service to refund credits."""
        url = f"{self._base_url}/api/v1/credits/refund"
        payload = {"user_id": str(user_id), "generation_id": str(generation_id), "amount": str(amount)}
        try:
            response = await self._http_client.post(url, json=payload, timeout=5.0)
            response.raise_for_status()
            logger.info(f"Successfully refunded {amount} credits for user {user_id} and generation {generation_id}")
        except httpx.RequestError as e:
            logger.error(f"Credit refund failed for user {user_id}: {e}", exc_info=True)
            # Log error but don't fail the entire process if refund fails.
            # This should be monitored via logs/alerts.