import uuid
from datetime import datetime, timedelta
from typing import Optional

from ....developer_platform.api.schemas import usage_schemas
from ....developer_platform.core import exceptions
from ....developer_platform.domain.models.usage import Quota, QuotaPeriod
from ....developer_platform.domain.repositories.quota_repository import IQuotaRepository
from ....developer_platform.domain.repositories.usage_repository import IUsageRepository


class QuotaManagementService:
    """
    Handles logic for checking, and managing API usage quotas.
    """

    def __init__(
        self, quota_repo: IQuotaRepository, usage_repo: IUsageRepository
    ):
        """
        Initializes the QuotaManagementService.

        Args:
            quota_repo: The repository for managing quota definitions.
            usage_repo: The repository for getting current usage data.
        """
        self.quota_repo = quota_repo
        self.usage_repo = usage_repo

    async def _get_or_create_default_quota(self, api_client_id: uuid.UUID, user_id: uuid.UUID) -> Quota:
        """Fetches the client's quota or creates a default one if it doesn't exist."""
        quota = await self.quota_repo.get_quota_by_client_id(api_client_id, user_id)
        if not quota:
            # In a real system, this would be based on the user's subscription tier.
            # For now, we'll create a default monthly quota.
            quota = Quota(
                api_client_id=api_client_id,
                user_id=user_id,
                limit_amount=1000,  # Default: 1000 generations per month
                period=QuotaPeriod.MONTHLY,
                last_reset_at=datetime.utcnow()
            )
            await self.quota_repo.save_quota(quota)
        return quota

    async def check_quota(
        self, api_client_id: uuid.UUID, user_id: uuid.UUID, action_cost: int = 1, action_type: str = "generation"
    ) -> bool:
        """
        Verifies if the client is within their quota for the current period
        before allowing an action. The actual decrement happens when usage is recorded.

        Args:
            api_client_id: The ID of the API client.
            user_id: The ID of the user owning the client.
            action_cost: The cost of the action to be performed (e.g., 1 for one generation).
            action_type: The type of action being checked (e.g., "generation").

        Returns:
            True if the action is allowed, False otherwise.

        Raises:
            InsufficientQuotaError: If the quota would be exceeded.
        """
        quota = await self._get_or_create_default_quota(api_client_id, user_id)

        # TODO: Implement logic to check if quota needs resetting
        # For simplicity, we assume a cron job handles resetting.

        current_usage = await self.usage_repo.get_count_for_period(
            api_client_id=api_client_id,
            period_start=quota.last_reset_at,
            action_type=action_type
        )

        if current_usage + action_cost > quota.limit_amount:
            raise exceptions.InsufficientQuotaError()

        return True

    async def get_quota_status(
        self, api_client_id: uuid.UUID, user_id: uuid.UUID, action_type: str = "generation"
    ) -> usage_schemas.QuotaStatusResponseSchema:
        """
        Returns the current quota status for a client.

        Args:
            api_client_id: The ID of the API client.
            user_id: The ID of the user owning the client.
            action_type: The type of action to get the quota status for.

        Returns:
            A DTO with the current quota status.
        """
        quota = await self._get_or_create_default_quota(api_client_id, user_id)

        # Calculate next reset time
        resets_at = None
        if quota.period == QuotaPeriod.MONTHLY:
            # This is a simplification; true monthly reset is more complex.
            resets_at = quota.last_reset_at + timedelta(days=30)
        elif quota.period == QuotaPeriod.DAILY:
            resets_at = quota.last_reset_at + timedelta(days=1)


        current_usage = await self.usage_repo.get_count_for_period(
            api_client_id=api_client_id,
            period_start=quota.last_reset_at,
            action_type=action_type
        )

        remaining = max(0, quota.limit_amount - current_usage)

        return usage_schemas.QuotaStatusResponseSchema(
            api_client_id=api_client_id,
            user_id=user_id,
            quota_type=action_type,
            limit=quota.limit_amount,
            remaining=remaining,
            period=quota.period.value,
            resets_at=resets_at
        )