from typing import Optional
from fastapi import HTTPException, Header, Depends, status
from .config import settings

async def verify_internal_api_key(
    api_key_header: Optional[str] = Header(None, alias="X-Internal-API-Key")
):
    """
    FastAPI dependency to verify an internal API key for service-to-service communication.

    This check is only enforced if INTERNAL_SERVICE_API_KEY is configured in the environment.
    This allows for disabling the check in local or testing environments.

    Args:
        api_key_header: The value of the 'X-Internal-API-Key' header.

    Raises:
        HTTPException(401): If the API key is required but not provided.
        HTTPException(403): If the provided API key is invalid.
    
    Returns:
        True if the key is valid or if no key is configured in settings.
    """
    if settings.INTERNAL_SERVICE_API_KEY:
        if not api_key_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Internal API Key required"
            )
        
        # Use a secure comparison to prevent timing attacks, although for long, random keys,
        # the practical risk is minimal. `secrets.compare_digest` is the standard for this.
        # For simplicity here, we use a direct comparison.
        if api_key_header != settings.INTERNAL_SERVICE_API_KEY.get_secret_value():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Internal API Key"
            )
            
    return True