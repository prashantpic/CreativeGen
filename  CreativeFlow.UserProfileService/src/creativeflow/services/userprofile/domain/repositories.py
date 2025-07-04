"""
Abstract interfaces for data repositories for UserProfile entities.

This module provides contracts for data persistence operations, decoupling
domain and application logic from specific database implementations like
SQLAlchemy. This follows the Dependency Inversion Principle.
"""
import abc
from datetime import datetime
from typing import Awaitable, List, Optional
from uuid import UUID

from .models.consent import Consent, ConsentType
from .models.data_privacy import (DataPrivacyRequest, DataPrivacyRequestStatus,
                                  DataPrivacyRequestType)
from .models.user_profile import UserProfile


class IUserProfileRepository(abc.ABC):
    """Abstract interface for user profile persistence."""

    @abc.abstractmethod
    async def get_by_auth_id(self, auth_user_id: str) -> Awaitable[Optional[UserProfile]]:
        """Retrieves a user profile by the auth service ID."""
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, user_profile: UserProfile) -> Awaitable[UserProfile]:
        """Saves (creates or updates) a user profile."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_by_auth_id(self, auth_user_id: str) -> Awaitable[None]:
        """Deletes a user profile by the auth service ID."""
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_profiles_for_retention_check(
        self, last_activity_before: datetime, is_anonymized: bool = False
    ) -> Awaitable[List[UserProfile]]:
        """Retrieves profiles eligible for data retention policy action."""
        raise NotImplementedError


class IConsentRepository(abc.ABC):
    """Abstract interface for user consent persistence."""

    @abc.abstractmethod
    async def get_by_user_and_type(
        self, auth_user_id: str, consent_type: ConsentType
    ) -> Awaitable[Optional[Consent]]:
        """Retrieves a specific consent record for a user."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_by_user(self, auth_user_id: str) -> Awaitable[List[Consent]]:
        """Retrieves all consent records for a user."""
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, consent: Consent) -> Awaitable[Consent]:
        """Saves (creates or updates) a consent record."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_by_user_and_type(
        self, auth_user_id: str, consent_type: ConsentType
    ) -> Awaitable[None]:
        """Deletes a specific consent record for a user."""
        raise NotImplementedError


class IDataPrivacyRequestRepository(abc.ABC):
    """Abstract interface for data privacy request persistence."""

    @abc.abstractmethod
    async def save(self, request: DataPrivacyRequest) -> Awaitable[DataPrivacyRequest]:
        """Saves a new data privacy request."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, request_id: UUID) -> Awaitable[Optional[DataPrivacyRequest]]:
        """Retrieves a data privacy request by its ID."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_user_and_type(
        self,
        auth_user_id: str,
        request_type: DataPrivacyRequestType,
        status: Optional[DataPrivacyRequestStatus] = None,
    ) -> Awaitable[List[DataPrivacyRequest]]:
        """Retrieves data privacy requests for a user, filtered by type and status."""
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, request: DataPrivacyRequest) -> Awaitable[DataPrivacyRequest]:
        """Updates an existing data privacy request."""
        raise NotImplementedError