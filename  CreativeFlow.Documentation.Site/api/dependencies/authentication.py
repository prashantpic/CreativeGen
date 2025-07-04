```python
import uuid
from typing import Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from application.services.api_key_service import APIKeyService
from core.config import get_settings
from core.exceptions import APIKeyInvalidError, NotAuthenticatedError
from domain.models.api_key import APIKey as APIKeyDomainModel

from .common import get_api_key_service

settings = get_settings()

api_key_header_scheme = APIKeyHeader(name=settings.API_KEY_HEADER_NAME, auto_error=False)


async def get_current_active_api_client(
    api_key_header_val: Optional[str] = Security(api_key_header_scheme),
    api_key_service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyDomainModel:
    """
    FastAPI dependency to authenticate and retrieve the active API client.
    
    Validates the API key from the header, checks if it's active,
    and returns the corresponding domain model.

    Raises:
        APIKeyInvalidError: If the API key is missing, invalid, or inactive.
    """
    if not api_key_header_val:
        raise APIKeyInvalidError("API key header is missing.")

    api_client = await api_key_service.validate_key(key_value=api_key_header_val)

    if not api_client:
        raise APIKeyInvalidError()

    if not api_client.is_active:
        raise APIKeyInvalidError("API Key is inactive.")

    return api_client


# --- Placeholder for User Authentication ---
# In a real application, this would involve validating a JWT token
# provided by the web application's session, likely in a cookie or
# Authorization header. The token would be decoded and validated against
# an authentication service to get the user's details.

class AuthenticatedUser(BaseModel):
    """
    Represents a user authenticated via the web application (e.g., JWT).
    This is a placeholder/mock implementation.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str = "developer@creativeflow.ai"
    # In a real scenario, this would include roles, permissions, etc.


async def get_current_authenticated_user() -> AuthenticatedUser:
    """
    Placeholder dependency to simulate an authenticated user for management endpoints.

    In a real system, this would:
    1. Extract a JWT from the request's Authorization header or cookie.
    2. Call an Authentication service to validate the token.
    3. Return the user's data upon successful validation.
    
    Raises:
        NotAuthenticatedError: If the token is invalid or missing.
    """
    # For now, we return a mock user.
    # To simulate a failure, you could raise NotAuthenticatedError().
    return AuthenticatedUser()
```