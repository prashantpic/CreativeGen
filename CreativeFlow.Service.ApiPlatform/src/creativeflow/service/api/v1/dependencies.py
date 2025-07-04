import logging

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from creativeflow.service.db.models.api_client import APIClient
from creativeflow.service.db.repository.api_client_repository import APIClientRepository
from creativeflow.service.db.session import AsyncSession, get_db_session
from creativeflow.service.service.quota_service import QuotaService

logger = logging.getLogger(__name__)

# Define the security scheme for the API Key in the "Authorization" header.
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)


async def get_current_api_client(
    api_key: str = Security(api_key_scheme),
    db: AsyncSession = Depends(get_db_session),
    api_client_repo: APIClientRepository = Depends(),
) -> APIClient:
    """
    FastAPI dependency to authenticate and retrieve the current API client.

    It extracts the API key from the 'Authorization' header, validates it against
    the database, and returns the corresponding active APIClient object.

    Raises:
        HTTPException(401): If the API key is missing.
        HTTPException(403): If the API key is invalid or inactive.

    Returns:
        The authenticated and active APIClient object.
    """
    if not api_key:
        logger.warning("API Key missing from request.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key required in Authorization header",
            headers={"WWW-Authenticate": "Header"},
        )

    client = await api_client_repo.get_by_api_key(db, api_key=api_key)

    if not client:
        logger.warning(f"Invalid or inactive API Key provided: {api_key[:6]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or inactive API Key",
        )

    return client


async def verify_usage_quota(
    api_client: APIClient = Depends(get_current_api_client),
    quota_service: QuotaService = Depends(),
) -> APIClient:
    """
    FastAPI dependency that chains authentication with quota verification.

    This dependency first authenticates the API client using `get_current_api_client`
    and then calls the `QuotaService` to check for rate limits and usage quotas.
    The `QuotaService` itself will raise the appropriate HTTP exceptions if
    limits are exceeded (e.g., 429 Too Many Requests, 402 Payment Required).

    Returns:
        The authenticated APIClient object if all checks pass.
    """
    await quota_service.check_and_log_usage(api_client=api_client)
    return api_client