import logging

from fastapi import Depends, HTTPException, status

from creativeflow.service.db.models.api_client import APIClient
from creativeflow.service.integrations.odoo_business_client import OdooBusinessClient

logger = logging.getLogger(__name__)


class QuotaService:
    """
    Service responsible for enforcing usage quotas and rate limits for API clients.
    """

    def __init__(self, odoo_client: OdooBusinessClient = Depends()):
        """
        Initializes the QuotaService with its dependencies.

        Args:
            odoo_client: An HTTP client to communicate with the Odoo Business Service.
                         This is injected by FastAPI's dependency system.
        """
        self.odoo_client = odoo_client

    async def check_and_log_usage(self, *, api_client: APIClient):
        """
        Performs the main quota and rate limiting check for an API call.

        This method coordinates checks for rate limits and credit/quota balance.
        If all checks pass, it logs the usage to deduct credits.

        Args:
            api_client: The authenticated APIClient object making the request.

        Raises:
            HTTPException(429): If the rate limit is exceeded.
            HTTPException(402): If the user has insufficient credits or quota.
            HTTPException(503): If the billing service is unavailable.
        """
        # 1. Rate Limiting Check (Placeholder)
        # This would typically be implemented using a fast in-memory store like Redis.
        # Example using a token bucket or fixed window algorithm.
        # For now, we will skip this and proceed to the quota check.
        # If rate limit were exceeded:
        # raise HTTPException(
        #     status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        #     detail="Rate limit exceeded. Please try again later."
        # )
        logger.info(f"Rate limit check passed (placeholder) for user {api_client.user_id}")

        # 2. Quota/Credit Check via Odoo Business Service
        try:
            quota_info = await self.odoo_client.check_user_quota(user_id=api_client.user_id)
            if not quota_info.get("can_transact", False):
                logger.warning(
                    f"Insufficient quota for user {api_client.user_id}. "
                    f"Reason: {quota_info.get('reason', 'Not specified')}"
                )
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail=f"Insufficient credits or quota. {quota_info.get('message', '')}".strip(),
                )
            logger.info(f"Quota check passed for user {api_client.user_id}")
        except HTTPException as e:
            # Re-raise exceptions we know about
            raise e
        except Exception as e:
            logger.error(
                f"Could not check user quota for {api_client.user_id} due to an error with the business service: {e}",
                exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not verify usage quota. The billing service is temporarily unavailable."
            )

        # 3. Log Usage / Deduct Credit via Odoo Business Service
        try:
            # Here you might pass details about the specific API call
            usage_details = {"api_call": "generation", "cost": 1} # Example cost
            await self.odoo_client.log_api_usage(user_id=api_client.user_id, usage_details=usage_details)
            logger.info(f"Successfully logged API usage for user {api_client.user_id}")
        except Exception as e:
            logger.error(
                f"Failed to log API usage for user {api_client.user_id} after quota check: {e}",
                exc_info=True
            )
            # This is a critical failure. The user was allowed to proceed but billing may fail.
            # Depending on business rules, you might:
            # a) Let the request succeed and flag the account for reconciliation. (Current approach)
            # b) Fail the request with a 500 error.
            pass