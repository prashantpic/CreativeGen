"""
Service layer for handling user profile operations.
"""
from typing import Awaitable, Optional

from ...adapters.api.v1.schemas import (InitialProfileDataSchema,
                                        UserProfilePatchRequestSchema)
from ...application.schemas import UserProfileSchema
from ...domain.exceptions import ProfileNotFoundError
from ...domain.models import Preferences, UserProfile
from ...domain.repositories import IUserProfileRepository


class UserProfileService:
    """
    Orchestrates operations related to user profiles, such as creation,
    retrieval, updates, and preferences management.
    """

    def __init__(self, user_profile_repo: IUserProfileRepository):
        """
        Initializes the UserProfileService.

        Args:
            user_profile_repo: The repository for user profile data persistence.
        """
        self.user_profile_repo = user_profile_repo

    async def get_user_profile(self, auth_user_id: str) -> Awaitable[UserProfileSchema]:
        """
        Retrieves a user profile and records the activity.

        Args:
            auth_user_id: The unique identifier from the auth service.

        Raises:
            ProfileNotFoundError: If no profile is found for the given ID.

        Returns:
            The user profile data as a DTO.
        """
        profile = await self.user_profile_repo.get_by_auth_id(auth_user_id)
        if not profile:
            raise ProfileNotFoundError(f"Profile for auth_user_id {auth_user_id} not found.")

        profile.record_activity()
        await self.user_profile_repo.save(profile)

        return UserProfileSchema.model_validate(profile)

    async def create_or_get_user_profile(
        self, auth_user_id: str, initial_data: Optional[InitialProfileDataSchema] = None
    ) -> Awaitable[UserProfileSchema]:
        """
        Retrieves a profile if it exists, or creates a new one.

        This is useful for on-demand profile creation upon a user's first
        interaction with a feature that requires a profile.

        Args:
            auth_user_id: The user's unique identifier from the auth service.
            initial_data: Optional initial data for preferences.

        Returns:
            The existing or newly created user profile DTO.
        """
        existing_profile = await self.user_profile_repo.get_by_auth_id(auth_user_id)
        if existing_profile:
            return UserProfileSchema.model_validate(existing_profile)

        preferences = Preferences()
        if initial_data:
            if initial_data.language_preference:
                preferences.language_preference = initial_data.language_preference
            if initial_data.timezone:
                preferences.timezone = initial_data.timezone

        new_profile = UserProfile(
            auth_user_id=auth_user_id,
            preferences=preferences,
        )
        saved_profile = await self.user_profile_repo.save(new_profile)
        return UserProfileSchema.model_validate(saved_profile)

    async def update_user_profile(
        self, auth_user_id: str, patch_data: UserProfilePatchRequestSchema
    ) -> Awaitable[UserProfileSchema]:
        """
        Updates a user's profile with partial data (progressive profiling).

        Args:
            auth_user_id: The identifier of the user to update.
            patch_data: A schema containing the fields to update.

        Raises:
            ProfileNotFoundError: If the profile to update does not exist.

        Returns:
            The updated user profile DTO.
        """
        profile = await self.user_profile_repo.get_by_auth_id(auth_user_id)
        if not profile:
            raise ProfileNotFoundError(f"Profile for auth_user_id {auth_user_id} not found.")

        update_data = patch_data.model_dump(exclude_unset=True)

        # Separate profile details from preference details
        details_to_update = {
            k: v for k, v in update_data.items()
            if k in {"full_name", "username", "profile_picture_url"}
        }
        prefs_to_update = {
            k: v for k, v in update_data.items()
            if k in {"language_preference", "timezone", "ui_settings"}
        }

        if details_to_update:
            profile.update_details(**details_to_update)
        
        if prefs_to_update:
            profile.update_preferences(**prefs_to_update)

        profile.record_activity()
        updated_profile = await self.user_profile_repo.save(profile)
        return UserProfileSchema.model_validate(updated_profile)