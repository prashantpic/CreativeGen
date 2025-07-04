```python
import logging
import secrets
import uuid
from typing import Dict, Optional, Tuple

from domain.models.api_key import APIKey, APIKeyPermissions
from domain.repositories.api_key_repository import IApiKeyRepository
from infrastructure.security import hashing

logger = logging.getLogger(__name__)

API_KEY_PREFIX = "cf_dev"
SECRET_LENGTH = 32  # 32 bytes = 256 bits of entropy
PREFIX_SEPARATOR = "_"


class APIKeyService:
    """
    Handles the business logic for API key management.
    """

    def __init__(self, api_key_repo: IApiKeyRepository):
        self.api_key_repo = api_key_repo

    async def generate_key(
        self, user_id: uuid.UUID, name: str, permissions: Optional[Dict] = None
    ) -> Tuple[APIKey, str]:
        """
        Generates a new API key and returns the domain model and the plaintext key.
        The plaintext key should only be shown to the user once.

        Returns:
            A tuple containing the APIKey domain model and the full plaintext API key.
        """
        key_prefix = f"{API_KEY_PREFIX}{PREFIX_SEPARATOR}{secrets.token_urlsafe(8)}"
        secret_part = secrets.token_urlsafe(SECRET_LENGTH)
        plaintext_key = f"{key_prefix}{PREFIX_SEPARATOR}{secret_part}"

        secret_hash = hashing.hash_secret(secret_part)

        key_permissions = APIKeyPermissions(**permissions) if permissions else APIKeyPermissions()

        api_key_domain = APIKey(
            user_id=user_id,
            name=name,
            key_prefix=key_prefix,
            secret_hash=secret_hash,
            permissions=key_permissions,
        )

        await self.api_key_repo.add(api_key_domain)
        logger.info(f"Generated new API key with ID {api_key_domain.id} for user {user_id}")
        return api_key_domain, plaintext_key

    async def validate_key(self, key_value: str) -> Optional[APIKey]:
        """
        Validates a full API key string (prefix + secret).

        Returns:
            The APIKey domain model if valid and active, otherwise None.
        """
        try:
            parts = key_value.split(PREFIX_SEPARATOR)
            if len(parts) != 3 or parts[0] != "cf" or parts[1] != "dev":
                return None
            
            key_prefix = f"{parts[0]}{PREFIX_SEPARATOR}{parts[1]}{PREFIX_SEPARATOR}{parts[2]}"
            secret_part = parts[3]
            
        except (IndexError, ValueError):
            logger.warning(f"Malformed API key provided: {key_value[:12]}...")
            return None

        api_key_domain = await self.api_key_repo.get_by_key_prefix(key_prefix)
        if not api_key_domain:
            return None

        if not api_key_domain.is_active:
            logger.warning(f"Authentication attempt with inactive API key ID: {api_key_domain.id}")
            return None

        if not hashing.verify_secret(secret_part, api_key_domain.secret_hash):
            logger.warning(f"Invalid secret provided for API key ID: {api_key_domain.id}")
            return None

        logger.debug(f"Successfully validated API key ID: {api_key_domain.id}")
        return api_key_domain

    async def list_keys_for_user(self, user_id: uuid.UUID) -> list[APIKey]:
        """Lists all API keys for a given user."""
        return await self.api_key_repo.list_by_user_id(user_id)

    async def get_key_by_id(self, api_key_id: uuid.UUID) -> Optional[APIKey]:
        """Retrieves a single API key by its database ID."""
        return await self.api_key_repo.get_by_id(api_key_id)

    async def revoke_key(self, api_key_id: uuid.UUID) -> Optional[APIKey]:
        """Revokes an API key, making it inactive."""
        key = await self.api_key_repo.get_by_id(api_key_id)
        if key:
            key.revoke()
            await self.api_key_repo.update(key)
            logger.info(f"Revoked API key with ID {api_key_id}")
            return key
        return None

    async def update_key(
        self,
        api_key_id: uuid.UUID,
        name: Optional[str],
        permissions: Optional[Dict],
        is_active: Optional[bool],
    ) -> Optional[APIKey]:
        """Updates the properties of an API key."""
        key = await self.api_key_repo.get_by_id(api_key_id)
        if not key:
            return None

        update_made = False
        if name is not None and key.name != name:
            key.name = name
            update_made = True
        if permissions is not None:
            key.permissions = APIKeyPermissions(**permissions)
            update_made = True
        if is_active is not None and key.is_active != is_active:
            key.is_active = is_active
            if not is_active:  # If we are deactivating, call revoke to set timestamp
                key.revoke()
            update_made = True

        if update_made:
            await self.api_key_repo.update(key)
            logger.info(f"Updated API key with ID {api_key_id}")
            
        return key
```