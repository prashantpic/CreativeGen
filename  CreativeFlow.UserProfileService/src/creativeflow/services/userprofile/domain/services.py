"""
Domain services for UserProfile-related business logic.

This module encapsulates complex domain logic that doesn't naturally fit
within a single entity, such as evaluating data retention policies that
involve both a UserProfile and a set of rules.
"""
from datetime import datetime, timedelta, timezone
from typing import Awaitable, List

from ..domain.models import RetentionRule, UserProfile
from ..domain.repositories import IUserProfileRepository


class DataRetentionPolicyService:
    """
    Encapsulates logic for evaluating data retention policies against a user profile.
    """

    def __init__(self, user_profile_repo: IUserProfileRepository):
        """
        Initializes the service with a user profile repository.

        Args:
            user_profile_repo: The repository for persisting profile changes.
        """
        self.user_profile_repo = user_profile_repo

    async def apply_policy_to_profile(
        self, user_profile: UserProfile, rules: List[RetentionRule]
    ) -> Awaitable[bool]:
        """
        Determines if a profile needs action based on rules and applies it.

        Iterates through retention rules and applies the first one that matches
        the profile's state (e.g., inactivity period).

        Args:
            user_profile: The user profile domain entity to evaluate.
            rules: A list of retention rules to check against.

        Returns:
            True if a retention action was taken, False otherwise.
        """
        if user_profile.is_anonymized:
            return False

        for rule in rules:
            # This is a simplified check. A real implementation might be more complex
            # and depend on the rule's 'basis' field.
            if rule.basis == "last_activity":
                cutoff_date = datetime.now(timezone.utc) - timedelta(
                    days=rule.retention_period_days
                )
                if user_profile.last_activity_at < cutoff_date:
                    if rule.action == "anonymize":
                        user_profile.anonymize()
                        await self.user_profile_repo.save(user_profile)
                        return True
                    elif rule.action == "delete":
                        await self.user_profile_repo.delete_by_auth_id(
                            user_profile.auth_user_id
                        )
                        return True
        return False