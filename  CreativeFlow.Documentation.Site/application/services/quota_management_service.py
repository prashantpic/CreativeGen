```python
import logging
import uuid
from datetime import datetime, timezone

from api.schemas.usage_schemas import QuotaStatusResponseSchema
from core.exceptions import InsufficientQuotaError
from domain.repositories.quota_repository import IQuotaRepository
from domain.repositories.usage_repository import IUsageRepository

logger = logging.getLogger(__name__)


class QuotaManagementService:
    """
    Handles business logic for checking and managing API usage quotas.
    """

    def __init__(
        self, quota_repo: IQuotaRepository, usage_repo: IUsageRepository
    ):
        self.quota_repo = quota_repo
        self.usage_repo = usage_repo

    async def check_quota(
        self, api_client_id: uuid.UUID, user_id: uuid.UUID, action_cost: int = 1
    ) -> bool:
        """
        Checks if the client has enough quota remaining for an action.
        This is a non-decrementing check. The decrement happens implicitly
        when UsageTrackingService records the call.

        Returns:
            True if the action can proceed, False otherwise.
        """
        quota = await self.quota_repo.get_quota_for_client(user_id=user_id)
        if not quota:
            # No specific quota found, policy could be to allow or deny.
            # For this example, we assume no quota means unlimited.
            logger.warning(f"No quota configuration found for user {user_id}. Allowing action.")
            return True

        # Check if the quota period has reset
        now = datetime.now(timezone.utc)
        if quota.should_reset(now):
            # In a real system, a background job would reset this.
            # For simplicity, we can log and proceed as if it were reset.
            logger.info(f"Quota for user {user_id} is due for a reset.")
            # We don't modify the quota here, just calculate usage from reset time.
            current_usage = await self.usage_repo.get_count_for_period(
                user_id=user_id,
                period_start=quota.get_current_period_start(now)
            )
        else:
             current_usage = await self.usage_repo.get_count_for_period(
                user_id=user_id,
                period_start=quota.last_reset_at
            )

        if (current_usage + action_cost) > quota.limit_amount:
            logger.warning(f"Quota check failed for user {user_id}. Usage: {current_usage}, Limit: {quota.limit_amount}")
            return False

        return True

    async def get_quota_status(
        self, api_client_id: uuid.UUID, user_id: uuid.UUID
    ) -> QuotaStatusResponseSchema:
        """
        Retrieves the current quota status for a client.
        """
        quota = await self.quota_repo.get_quota_for_client(user_id=user_id)
        if not quota:
            # Return a default "unlimited" status if no quota is set
            return QuotaStatusResponseSchema(
                api_client_id=api_client_id,
                user_id=user_id,
                quota_type="generations",
                limit=-1, # -1 signifies unlimited
                remaining=-1,
                period="N/A",
                resets_at=None,
            )
        
        now = datetime.now(timezone.utc)
        period_start = quota.get_current_period_start(now)
        
        current_usage = await self.usage_repo.get_count_for_period(
            user_id=user_id, period_start=period_start
        )

        remaining = quota.limit_amount - current_usage

        return QuotaStatusResponseSchema(
            api_client_id=api_client_id,
            user_id=user_id,
            quota_type="generations",  # This could be dynamic in a more complex system
            limit=quota.limit_amount,
            remaining=max(0, remaining),
            period=quota.period.value,
            resets_at=quota.get_next_reset_time(now),
        )
```