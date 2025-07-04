"""
FastAPI dependencies for database sessions, service instantiation, and user authentication.

This module provides common dependencies to be injected into API endpoint handlers,
promoting code reuse and separation of concerns.
"""
from typing import AsyncGenerator, Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....application.services.consent_service import ConsentService
from ....application.services.data_privacy_service import DataPrivacyService
from ....application.services.user_profile_service import UserProfileService
from ...db.database import get_async_db_session
from ...db.repositories.consent_repository import SQLAlchemyConsentRepository
from ...db.repositories.data_privacy_request_repository import \
    SQLAlchemyDataPrivacyRequestRepository
from ...db.repositories.user_profile_repository import \
    SQLAlchemyUserProfileRepository
from ....domain.repositories import (IConsentRepository,
                                     IDataPrivacyRequestRepository,
                                     IUserProfileRepository)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an SQLAlchemy `AsyncSession`.
    Ensures the session is properly closed after the request.
    """
    async for session in get_async_db_session():
        yield session


def get_user_profile_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> IUserProfileRepository:
    """Dependency to get an instance of the user profile repository."""
    return SQLAlchemyUserProfileRepository(db_session)


def get_consent_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> IConsentRepository:
    """Dependency to get an instance of the consent repository."""
    return SQLAlchemyConsentRepository(db_session)


def get_data_privacy_request_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> IDataPrivacyRequestRepository:
    """Dependency to get an instance of the data privacy request repository."""
    return SQLAlchemyDataPrivacyRequestRepository(db_session)


def get_user_profile_service(
    repo: IUserProfileRepository = Depends(get_user_profile_repository),
) -> UserProfileService:
    """Dependency to get an instance of the UserProfileService."""
    return UserProfileService(user_profile_repo=repo)


def get_consent_service(
    repo: IConsentRepository = Depends(get_consent_repository),
) -> ConsentService:
    """Dependency to get an instance of the ConsentService."""
    return ConsentService(consent_repo=repo)


def get_data_privacy_service(
    profile_repo: IUserProfileRepository = Depends(get_user_profile_repository),
    privacy_repo: IDataPrivacyRequestRepository = Depends(get_data_privacy_request_repository),
    consent_repo: IConsentRepository = Depends(get_consent_repository),
) -> DataPrivacyService:
    """Dependency to get an instance of the DataPrivacyService."""
    return DataPrivacyService(
        user_profile_repo=profile_repo,
        privacy_request_repo=privacy_repo,
        consent_repo=consent_repo,
    )


async def get_current_auth_user_id(
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
) -> str:
    """
    Dependency to get the authenticated user's ID from a trusted header.

    This assumes an upstream service (like an API Gateway) has already
    validated the user's JWT and is passing the user ID in this header.
    """
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not provided in headers",
        )
    return x_user_id