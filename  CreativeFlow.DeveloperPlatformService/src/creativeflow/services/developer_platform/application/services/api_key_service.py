import secrets
import uuid
from typing import Dict, List, Optional, Tuple

from ....developer_platform.core import exceptions
from ....developer_platform.domain.models.api_key import APIKey as APIKeyDomainModel
from ....developer_platform.domain.models.api_key import APIKeyPermissions
from ....developer_platform.domain.repositories.api_key_repository import IApiKeyRepository
from ....developer_platform.infrastructure.security import hashing

API_KEY_PREFIX = "cf_dev"
SECRET_LENGTH = 32


class APIKeyService:
    """
    Handles business logic for API key generation, validation, revocation,
    and permission management.
    """

    def __init__(self, api_key_repo: IApiKeyRepository):
        """
        Initializes the APIKeyService.

        Args:
            api_key_repo: The repository for accessing API key data.
        """
        self.api_key_repo = api_key_repo

    async def generate_key(
        self, user_id: uuid.UUID, name: str, permissions: Optional[Dict[str, bool]] = None
    ) -> Tuple[APIKeyDomainModel, str]:
        """
        Generates a new API key and secret.

        The plaintext secret is only returned once upon creation.

        Args:
            user_id: The ID of the user creating the key.
            name: A user-friendly name for the key.
            permissions: A dictionary of permissions for the key.

        Returns:
            A tuple containing the created APIKey domain model and the
            plaintext API key string (prefix_secret).
        """
        key_prefix = f"{API_KEY_PREFIX}_{secrets.token_urlsafe(8)}"
        secret = secrets.token_urlsafe(SECRET_LENGTH)
        full_key = f"{key_prefix}_{secret}"
        secret_hash = hashing.hash_secret(secret)

        key_permissions = APIKeyPermissions(**permissions) if permissions else APIKeyPermissions()

        api_key_domain = APIKeyDomainModel(
            user_id=user_id,
            name=name,
            key_prefix=key_prefix,
            secret_hash=secret_hash,
            permissions=key_permissions,
        )

        await self.api_key_repo.add(api_key_domain)
        return api_key_domain, full_key

    async def validate_key(self, key_value: str) -> Optional[APIKeyDomainModel]:
        """
        Validates a full API key string (prefix_secret).

        It splits the key, finds the key by its prefix, and verifies the secret.

        Args:
            key_value: The full API key string to validate.

        Returns:
            The APIKey domain model if valid and active, otherwise None.
        """
        try:
            prefix, secret = key_value.rsplit("_", 1)
        except ValueError:
            return None  # Invalid key format

        key_domain = await self.api_key_repo.get_by_key_prefix(key_prefix=prefix)

        if not key_domain:
            return None

        if not key_domain.is_active:
            raise exceptions.APIKeyInactiveError()

        if not hashing.verify_secret(secret, key_domain.secret_hash):
            return None

        return key_domain

    async def revoke_key(self, api_key_id: uuid.UUID, user_id: uuid.UUID) -> APIKeyDomainModel:
        """
        Revokes an API key.

        Args:
            api_key_id: The ID of the API key to revoke.
            user_id: The ID of the user making the request, for authorization.

        Returns:
            The revoked APIKey domain model.

        Raises:
            APIKeyNotFoundError: If the key is not found or not owned by the user.
        """
        key_domain = await self.get_key_by_id(api_key_id, user_id)
        key_domain.revoke()
        await self.api_key_repo.update(key_domain)
        return key_domain

    async def list_keys_for_user(self, user_id: uuid.UUID) -> List[APIKeyDomainModel]:
        """
        Lists all non-revoked API keys for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of APIKey domain models.
        """
        return await self.api_key_repo.list_by_user_id(user_id=user_id)

    async def get_key_by_id(self, api_key_id: uuid.UUID, user_id: uuid.UUID) -> APIKeyDomainModel:
        """
        Retrieves a single API key by its ID, ensuring user ownership.

        Args:
            api_key_id: The ID of the API key.
            user_id: The ID of the user making the request.

        Returns:
            The APIKey domain model.

        Raises:
            APIKeyNotFoundError: If the key is not found or not owned by the user.
        """
        key_domain = await self.api_key_repo.get_by_id(api_key_id=api_key_id)
        if not key_domain or key_domain.user_id != user_id:
            raise exceptions.APIKeyNotFoundError()
        return key_domain

    async def update_key(
        self,
        api_key_id: uuid.UUID,
        user_id: uuid.UUID,
        name: Optional[str] = None,
        permissions: Optional[Dict[str, bool]] = None,
        is_active: Optional[bool] = None,
    ) -> APIKeyDomainModel:
        """
        Updates an API key's details.

        Args:
            api_key_id: The ID of the API key to update.
            user_id: The ID of the user making the request.
            name: The new name for the key.
            permissions: The new permissions for the key.
            is_active: The new active status for the key.

        Returns:
            The updated APIKey domain model.
        """
        key_domain = await self.get_key_by_id(api_key_id, user_id)

        if name is not None:
            key_domain.name = name
        if permissions is not None:
            key_domain.permissions = APIKeyPermissions(**permissions)
        if is_active is not None:
            key_domain.is_active = is_active

        await self.api_key_repo.update(key_domain)
        return key_domain