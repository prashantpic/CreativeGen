from typing import Optional
import uuid
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field

from core.config import get_settings
from application.services.api_key_service import APIKeyService
from domain.models.api_key import APIKey as APIKeyDomainModel
from .common import get_api_key_service

settings = get_settings()

api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER_NAME, auto_error=False)


async def get_current_active_api_client(
    api_key_header_val: str = Security(api_key_header),
    api_key_service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyDomainModel:
    """
    Authenticates and retrieves the active API client based on the provided API key.

    This dependency extracts the API key from the request header, validates it,
    and ensures the corresponding client is active.

    Args:
        api_key_header_val: The API key value from the 'X-API-KEY' header.
        api_key_service: The service responsible for API key business logic.

    Raises:
        HTTPException(401): If the API key is missing, invalid, or inactive.

    Returns:
        The authenticated and active APIKey domain model.
    """
    if not api_key_header_val:
        raise HTTPException(
            status_code=401, detail="API Key is missing"
        )

    api_client = await api_key_service.validate_key(key_value=api_key_header_val)

    if not api_client:
        raise HTTPException(
            status_code=401, detail="Invalid or inactive API Key"
        )
    
    # The validate_key service method already checks for activity.
    # An additional check here is for defense-in-depth.
    if not api_client.is_active:
         raise HTTPException(
            status_code=401, detail="API Key is inactive"
        )

    return api_client


# --- Placeholder for User Authentication ---
# In a real-world scenario, this dependency would validate a JWT token
# from a user's web session and return a detailed user object.
# For this service, we only need a mock that provides a user ID for
# authorization purposes on management endpoints.

class AuthenticatedUser(BaseModel):
    """
    A placeholder model representing an authenticated user.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="The authenticated user's unique ID.")
    # Add other fields like email, roles, etc. as needed from a real JWT payload.


async def get_current_authenticated_user() -> AuthenticatedUser:
    """
    Placeholder dependency to simulate an authenticated user session.

    This would typically involve decoding a JWT from an Authorization header,
    verifying its signature and claims, and fetching user details.

    For now, it returns a mock user object with a static UUID.

    Returns:
        A mock AuthenticatedUser object.
    """
    # In a real implementation:
    # 1. Get token from `Authorization: Bearer <token>` header.
    # 2. Decode and validate the JWT using a library like python-jose.
    # 3. Raise HTTPException(401) or 403 if invalid.
    # 4. Return user data from token payload.
    return AuthenticatedUser(id=uuid.UUID("a7f8c9d0-1234-5678-abcd-ef1234567890"))