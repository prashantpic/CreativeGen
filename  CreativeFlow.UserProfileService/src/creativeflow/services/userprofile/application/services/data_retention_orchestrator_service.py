"""
Orchestrates the application of data retention policies to user profiles.
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Awaitable, List

from ...domain.models import RetentionRule, RetentionRuleAction
from ...domain.repositories import IUserProfileRepository
from ...domain.services import DataRetentionPolicyService

logger = logging.getLogger(__name__)


class DataRetentionOrchestratorService:
    """
    Periodically (e.g., via a scheduled job) applies data retention policies.
    """

    def __init__(
        self,
        user_profile_repo: IUserProfileRepository,
        retention_policy_service: DataRetentionPolicyService,
    ):
        """
        Initializes the service.

        Args:
            user_profile_repo: The repository for fetching profiles.
            retention_policy_service: The domain service containing policy logic.
        """
        self.user_profile_repo = user_profile_repo
        self.retention_policy_service = retention_policy_service

    async def apply_retention_policies_globally(self) -> Awaitable[None]:
        """
        Fetches eligible profiles and applies defined retention policies.

        This method is designed to be called by a scheduler (e.g., a cron job)
        to perform routine data cleanup and anonymization based on inactivity.
        """
        logger.info("Starting global data retention policy application.")

        # In a real system, these rules might come from a configuration file
        # or a database table.
        rules = [
            RetentionRule(
                data_category="inactive_user_profile",
                retention_period_days=730,  # 2 years
                action=RetentionRuleAction.ANONYMIZE,
                basis="last_activity",
            )
        ]

        # For this example, we only process the first rule.
        # A more complex system might handle multiple rules and categories.
        if not rules:
            logger.info("No retention rules defined. Exiting.")
            return

        rule = rules[0]
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=rule.retention_period_days)
        
        logger.info(f"Fetching profiles with last activity before {cutoff_date} for anonymization.")

        eligible_profiles = await self.user_profile_repo.get_profiles_for_retention_check(
            last_activity_before=cutoff_date, is_anonymized=False
        )

        if not eligible_profiles:
            logger.info("No profiles found that are eligible for retention action.")
            return

        logger.info(f"Found {len(eligible_profiles)} profiles for retention processing.")
        
        processed_count = 0
        for profile in eligible_profiles:
            try:
                action_taken = await self.retention_policy_service.apply_policy_to_profile(
                    profile, rules
                )
                if action_taken:
                    logger.info(
                        f"Retention policy applied to profile for auth_user_id: {profile.auth_user_id}"
                    )
                    processed_count += 1
            except Exception as e:
                logger.error(
                    f"Error applying retention policy to profile for "
                    f"auth_user_id {profile.auth_user_id}: {e}",
                    exc_info=True,
                )

        logger.info(
            f"Finished global data retention policy application. "
            f"Processed {processed_count}/{len(eligible_profiles)} profiles."
        )