"""
Contains security-related utility functions for the MLOps service.

This module provides helpers for authentication and authorization, such as
validating API keys for internal service-to-service communication.
"""
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette import status

from creativeflow.mlops_service.core.config import get_settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verifies the provided API key for service-to-service authentication.

    This function is intended to be used as a FastAPI dependency to protect
    internal API endpoints.

    Args:
        api_key: The API key passed in the request header.

    Raises:
        HTTPException: If the API key is invalid.
    """
    settings = get_settings()
    expected_api_key = settings.INTERNAL_API_KEY.get_secret_value()

    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )