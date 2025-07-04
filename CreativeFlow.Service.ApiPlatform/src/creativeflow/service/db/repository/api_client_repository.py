import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from creativeflow.service.db.models.api_client import APIClient
from creativeflow.service.api.v1.schemas.api_key_schemas import APIKeyCreateSchema


class APIClientRepository:
    """
    Encapsulates database access logic for the APIClient model.
    Follows the Repository Pattern to abstract data layer from the service layer.
    """

    async def get_by_api_key(self, db: AsyncSession, *, api_key: str) -> Optional[APIClient]:
        """
        Retrieves an active APIClient by its public API key.

        Args:
            db: The async database session.
            api_key: The public API key to search for.

        Returns:
            The APIClient object if found and active, otherwise None.
        """
        stmt = select(APIClient).where(APIClient.api_key == api_key, APIClient.is_active == True)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: APIKeyCreateSchema,
        user_id: uuid.UUID,
        api_key: str,
        secret_hash: str
    ) -> APIClient:
        """
        Creates a new APIClient record in the database.

        Args:
            db: The async database session.
            obj_in: Pydantic schema with input data (e.g., name).
            user_id: The ID of the user creating the key.
            api_key: The generated public API key.
            secret_hash: The hashed secret for the API key.

        Returns:
            The newly created APIClient object.
        """
        db_obj = APIClient(
            name=obj_in.name,
            user_id=user_id,
            api_key=api_key,
            secret_hash=secret_hash,
            permissions=obj_in.permissions
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def revoke(self, db: AsyncSession, *, db_obj: APIClient) -> APIClient:
        """
        Revokes an API key by setting its `is_active` flag to False.

        Args:
            db: The async database session.
            db_obj: The APIClient instance to revoke.

        Returns:
            The updated (revoked) APIClient object.
        """
        db_obj.is_active = False
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id_and_user(
        self, db: AsyncSession, *, key_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[APIClient]:
        """
        Retrieves an APIClient by its ID, ensuring it belongs to the specified user.
        """
        stmt = select(APIClient).where(APIClient.id == key_id, APIClient.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def list_by_user(self, db: AsyncSession, *, user_id: uuid.UUID) -> list[APIClient]:
        """
        Lists all active API keys for a specific user.
        """
        stmt = select(APIClient).where(APIClient.user_id == user_id, APIClient.is_active == True)
        result = await db.execute(stmt)
        return list(result.scalars().all())