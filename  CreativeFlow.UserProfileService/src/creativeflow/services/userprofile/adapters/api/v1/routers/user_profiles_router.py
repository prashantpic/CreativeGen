"""
HTTP endpoints for user profile management.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Path, status

from .....application.services.user_profile_service import UserProfileService
from ..dependencies import get_user_profile_service
from ..schemas import (InitialProfileDataSchema, UserProfilePatchRequestSchema,
                       UserProfileResponseSchema)

router = APIRouter()


@router.get(
    "/{auth_user_id}",
    response_model=UserProfileResponseSchema,
    summary="Get User Profile",
    description="Retrieve a user's complete profile by their authentication ID.",
)
async def get_user_profile_endpoint(
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    service: UserProfileService = Depends(get_user_profile_service),
) -> UserProfileResponseSchema:
    """
    Endpoint to retrieve a user's profile.
    """
    return await service.get_user_profile(auth_user_id=auth_user_id)


@router.post(
    "/{auth_user_id}",
    response_model=UserProfileResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create or Get User Profile",
    description="Creates a new user profile if one doesn't exist for the given auth_user_id, or retrieves the existing one.",
)
async def create_user_profile_endpoint(
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    initial_profile_data: Optional[InitialProfileDataSchema] = None,
    service: UserProfileService = Depends(get_user_profile_service),
) -> UserProfileResponseSchema:
    """
    Endpoint to create a user profile on first interaction, or get it if it exists.
    """
    return await service.create_or_get_user_profile(
        auth_user_id=auth_user_id, initial_data=initial_profile_data
    )


@router.patch(
    "/{auth_user_id}",
    response_model=UserProfileResponseSchema,
    summary="Partially Update User Profile",
    description="Update one or more fields of a user's profile. Ideal for progressive profiling.",
)
async def patch_user_profile_endpoint(
    profile_patch: UserProfilePatchRequestSchema,
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    service: UserProfileService = Depends(get_user_profile_service),
) -> UserProfileResponseSchema:
    """
    Endpoint for making partial updates to a user's profile.
    """
    return await service.update_user_profile(
        auth_user_id=auth_user_id, patch_data=profile_patch
    )