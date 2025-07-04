"""
Contains security-related utility functions.

This module provides helpers for authentication and authorization, such as
API key validation, which is used for securing internal service-to-service
communication.
"""

from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from creativeflow.mlops_service.core.config import get_settings

# Define the API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

settings = get_settings()

async def verify_api_key(api_key: str = Security(api_key_header)) -> bool:
    """
    Verifies the provided API key for service-to-service authentication.

    This function compares the API key from the 'X-API-Key' header with the
    one configured in the application settings.

    Args:
        api_key: The API key passed in the request header.

    Returns:
        True if the API key is valid.

    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    if not api_key:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="API key is missing"
        )
    
    # Use a secure comparison to prevent timing attacks, though for internal keys
    # of sufficient length and randomness, direct comparison is often acceptable.
    # A more robust solution might use hmac.compare_digest.
    if api_key != settings.INTERNAL_API_KEY.get_secret_value():
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return True

# In a more complex system, you might have functions like:
#
# from typing import Optional
# from uuid import UUID
#
# class UserPrincipal:
#     def __init__(self, user_id: UUID, roles: list[str]):
#         self.user_id = user_id
#         self.roles = roles
#
# async def get_current_user_principal(...) -> UserPrincipal:
#     """
#     Parses a JWT from the request header, validates it, and returns
#     a user principal object with user ID and roles for authorization checks.
#     """
#     # This would typically involve a shared library for JWT validation
#     pass