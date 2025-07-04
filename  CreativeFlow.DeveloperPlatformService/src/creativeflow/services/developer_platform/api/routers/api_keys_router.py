from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.authentication import get_current_authenticated_user, AuthenticatedUser
from api.dependencies.common import get_api_key_service
from api.schemas.api_key_schemas import (
    APIKeyCreateSchema,
    APIKeyCreateResponseSchema,
    APIKeyResponseSchema,
    APIKeyUpdateSchema
)
from api.schemas.base_schemas import StatusResponseSchema
from application.services.api_key_service import APIKeyService
from core.exceptions import APIKeyNotFoundError

# Management of API Keys requires an authenticated user session (e.g., from the developer portal).
router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
    dependencies=[Depends(get_current_authenticated_user)],
)


@router.post(
    "/",
    response_model=APIKeyCreateResponseSchema,
    status_code=201,
    summary="Create a new API Key",
    description="Generates a new API key and secret for the authenticated user. The secret is only returned once upon creation."
)
async def create_api_key(
    payload: APIKeyCreateSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyCreateResponseSchema:
    """
    Creates a new API key for the authenticated user.
    """
    key_domain, plaintext_secret = await service.generate_key(
        user_id=user.id,
        name=payload.name,
        permissions=payload.permissions,
    )
    
    full_api_key = f"{key_domain.key_prefix}_{plaintext_secret}"

    return APIKeyCreateResponseSchema(
        id=key_domain.id,
        name=key_domain.name,
        permissions=key_domain.permissions.model_dump(),
        key_prefix=key_domain.key_prefix,
        api_key=full_api_key,
        is_active=key_domain.is_active,
        created_at=key_domain.created_at,
    )


@router.get(
    "/",
    response_model=List[APIKeyResponseSchema],
    summary="List API Keys",
    description="Retrieves a list of all non-revoked API keys for the authenticated user."
)
async def list_api_keys(
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> List[APIKeyResponseSchema]:
    """
    Lists all API keys associated with the authenticated user.
    """
    keys = await service.list_keys_for_user(user_id=user.id)
    return [
        APIKeyResponseSchema.model_validate(key) for key in keys
    ]


@router.get(
    "/{api_key_id}",
    response_model=APIKeyResponseSchema,
    summary="Get API Key Details",
    description="Retrieves details for a specific API key belonging to the authenticated user."
)
async def get_api_key(
    api_key_id: UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyResponseSchema:
    """
    Retrieves details for a specific API key, ensuring it belongs to the user.
    """
    try:
        key = await service.get_key_by_id(api_key_id=api_key_id, user_id=user.id)
        return APIKeyResponseSchema.model_validate(key)
    except APIKeyNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put(
    "/{api_key_id}",
    response_model=APIKeyResponseSchema,
    summary="Update an API Key",
    description="Updates the name or permissions of a specific API key."
)
async def update_api_key(
    api_key_id: UUID,
    payload: APIKeyUpdateSchema,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyResponseSchema:
    """
    Updates an API key's properties, ensuring it belongs to the user.
    """
    try:
        updated_key = await service.update_key(
            api_key_id=api_key_id,
            user_id=user.id,
            update_data=payload.model_dump(exclude_unset=True)
        )
        return APIKeyResponseSchema.model_validate(updated_key)
    except APIKeyNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete(
    "/{api_key_id}",
    response_model=StatusResponseSchema,
    summary="Revoke an API Key",
    description="Revokes (deactivates) an API key, preventing it from being used for future requests."
)
async def revoke_api_key(
    api_key_id: UUID,
    user: AuthenticatedUser = Depends(get_current_authenticated_user),
    service: APIKeyService = Depends(get_api_key_service),
) -> StatusResponseSchema:
    """
    Revokes an API key, ensuring it belongs to the user.
    """
    try:
        await service.revoke_key(api_key_id=api_key_id, user_id=user.id)
        return StatusResponseSchema(status="success", message="API key has been revoked.")
    except APIKeyNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)