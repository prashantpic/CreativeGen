```python
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from api.dependencies.authentication import (
    AuthenticatedUser,
    get_current_authenticated_user,
)
from api.dependencies.common import get_api_key_service
from api.schemas.api_key_schemas import (
    APIKeyCreateRequestSchema,
    APIKeyCreateResponseSchema,
    APIKeyResponseSchema,
    APIKeyUpdateRequestSchema,
)
from api.schemas.base_schemas import StatusResponseSchema
from application.services.api_key_service import APIKeyService
from core.exceptions import ForbiddenError, APIKeyNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys (Management)"],
    dependencies=[Depends(get_current_authenticated_user)],
)


@router.post(
    "/",
    response_model=APIKeyCreateResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new API Key",
)
async def create_api_key(
    payload: APIKeyCreateRequestSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyCreateResponseSchema:
    """
    Generates a new API key for the authenticated user.

    The full API key value is returned **only once** upon creation.
    It must be stored securely by the user.
    """
    logger.info(f"User {user.id} creating API key with name '{payload.name}'.")
    key_domain, plaintext_key = await service.generate_key(
        user_id=user.id, name=payload.name, permissions=payload.permissions
    )
    return APIKeyCreateResponseSchema(
        id=key_domain.id,
        user_id=key_domain.user_id,
        name=key_domain.name,
        permissions=key_domain.permissions.model_dump() if key_domain.permissions else {},
        key_prefix=key_domain.key_prefix,
        api_key=plaintext_key,
        is_active=key_domain.is_active,
        created_at=key_domain.created_at,
        revoked_at=key_domain.revoked_at,
    )


@router.get(
    "/",
    response_model=List[APIKeyResponseSchema],
    summary="List all API Keys for the user",
)
async def list_api_keys(
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> List[APIKeyResponseSchema]:
    """
    Retrieves a list of all API keys belonging to the authenticated user.
    The secret part of the key is not included.
    """
    logger.info(f"User {user.id} requesting list of their API keys.")
    keys = await service.list_keys_for_user(user_id=user.id)
    return [APIKeyResponseSchema.model_validate(key) for key in keys]


@router.get(
    "/{api_key_id}",
    response_model=APIKeyResponseSchema,
    summary="Get a specific API Key",
)
async def get_api_key(
    api_key_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyResponseSchema:
    """
    Retrieves details for a single API key by its ID.
    Ensures the key belongs to the authenticated user.
    """
    logger.info(f"User {user.id} requesting details for API key {api_key_id}.")
    key = await service.get_key_by_id(api_key_id=api_key_id)
    if not key or key.user_id != user.id:
        raise APIKeyNotFoundError()
    return APIKeyResponseSchema.model_validate(key)


@router.put(
    "/{api_key_id}",
    response_model=APIKeyResponseSchema,
    summary="Update an API Key",
)
async def update_api_key(
    api_key_id: uuid.UUID,
    payload: APIKeyUpdateRequestSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyResponseSchema:
    """
    Updates the properties of an existing API key, such as its name,
    active status, or permissions.
    """
    logger.info(f"User {user.id} updating API key {api_key_id}.")
    # First, verify ownership
    key_to_update = await service.get_key_by_id(api_key_id=api_key_id)
    if not key_to_update or key_to_update.user_id != user.id:
        raise APIKeyNotFoundError()

    updated_key = await service.update_key(
        api_key_id=api_key_id,
        name=payload.name,
        permissions=payload.permissions,
        is_active=payload.is_active,
    )
    return APIKeyResponseSchema.model_validate(updated_key)


@router.delete(
    "/{api_key_id}",
    response_model=StatusResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Revoke an API Key",
)
async def revoke_api_key(
    api_key_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> StatusResponseSchema:
    """
    Permanently revokes an API key. This action is irreversible.
    The key will be marked as inactive and can no longer be used for authentication.
    """
    logger.info(f"User {user.id} revoking API key {api_key_id}.")
    key_to_revoke = await service.get_key_by_id(api_key_id)
    if not key_to_revoke:
        # To avoid leaking information, we can return a success response even if not found
        logger.warning(f"Attempt to revoke non-existent API key {api_key_id}.")
        return StatusResponseSchema(message="API Key revoked successfully.")

    if key_to_revoke.user_id != user.id:
        raise ForbiddenError("You can only revoke your own API keys.")

    await service.revoke_key(api_key_id=api_key_id)
    return StatusResponseSchema(message="API Key revoked successfully.")
```