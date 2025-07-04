"""
Service layer for managing AI Models and Model Versions in the registry.

This service encapsulates the business logic for model and version registration,
metadata management, and lifecycle state transitions, coordinating between the
API layer and the data access (repository) layer.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas import model_schemas
from creativeflow.mlops_service.domain.enums import ModelVersionStatusEnum
from creativeflow.mlops_service.infrastructure.database.orm_models import (
    AIModelORM, AIModelVersionORM
)
from creativeflow.mlops_service.infrastructure.database.repositories import (
    model_repository, version_repository
)
from creativeflow.mlops_service.utils.exceptions import InvalidStateTransitionException, ModelNotFoundException


class ModelRegistryService:
    """Handles business logic for model registration and versioning."""

    def __init__(self):
        self.model_repo = model_repository
        self.version_repo = version_repository

    async def create_model(self, db: Session, model_in: model_schemas.ModelCreateSchema) -> AIModelORM:
        """
        Creates a new AI Model record.

        Args:
            db: The database session.
            model_in: The Pydantic schema with model creation data.

        Returns:
            The created AIModelORM object.
        """
        return await self.model_repo.create(db, obj_in=model_in)

    async def get_model_by_id(self, db: Session, model_id: UUID) -> Optional[AIModelORM]:
        """
        Retrieves an AI Model by its ID.

        Args:
            db: The database session.
            model_id: The UUID of the model to retrieve.

        Returns:
            The AIModelORM object or None if not found.
        """
        return await self.model_repo.get(db, id=model_id)

    async def get_models(self, db: Session, skip: int, limit: int) -> List[AIModelORM]:
        """
        Lists all AI Models with pagination.

        Args:
            db: The database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of AIModelORM objects.
        """
        return await self.model_repo.get_multi(db, skip=skip, limit=limit)

    async def create_model_version(
        self,
        db: Session,
        model_id: UUID,
        version_in: model_schemas.ModelVersionCreateSchema,
        artifact_path: str,
        user_id: Optional[UUID]
    ) -> AIModelVersionORM:
        """
        Creates a new version for an existing model.

        Args:
            db: The database session.
            model_id: The UUID of the parent model.
            version_in: Pydantic schema with version creation data.
            artifact_path: The storage path of the model's artifact.
            user_id: The ID of the user creating the version.

        Returns:
            The created AIModelVersionORM object.
        """
        model = await self.model_repo.get(db, id=model_id)
        if not model:
            raise ModelNotFoundException(str(model_id))

        version_data = version_in.model_dump()
        version_data.update({
            "model_id": model_id,
            "artifact_path": artifact_path,
            "created_by_user_id": user_id,
            "status": ModelVersionStatusEnum.STAGING,
        })
        
        # This uses a temporary schema because the repository expects one,
        # but we've manually constructed the dict.
        # A more advanced repo might take a dict directly.
        create_schema = model_schemas.ModelVersionResponseSchema(**version_data, id=UUID('00000000-0000-0000-0000-000000000000'), created_at="2000-01-01")
        
        db_obj = AIModelVersionORM(**version_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    async def get_model_version_by_id(self, db: Session, version_id: UUID) -> Optional[AIModelVersionORM]:
        """
        Retrieves a specific AI Model Version by its ID.

        Args:
            db: The database session.
            version_id: The UUID of the model version.

        Returns:
            The AIModelVersionORM object or None if not found.
        """
        return await self.version_repo.get(db, id=version_id)

    async def get_versions_for_model(
        self, db: Session, model_id: UUID, skip: int, limit: int
    ) -> List[AIModelVersionORM]:
        """
        Lists all versions for a specific AI Model.

        Args:
            db: The database session.
            model_id: The UUID of the parent model.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of AIModelVersionORM objects.
        """
        return await self.version_repo.list_by_model_id(db, model_id=model_id, skip=skip, limit=limit)

    async def update_version_status(
        self, db: Session, version_id: UUID, new_status: ModelVersionStatusEnum
    ) -> AIModelVersionORM:
        """
        Updates the status of a model version.

        Implements logic for valid state transitions. For example, a model must
        be 'VALIDATED' before being moved to 'PRODUCTION'.

        Args:
            db: The database session.
            version_id: The UUID of the model version to update.
            new_status: The target status.

        Returns:
            The updated AIModelVersionORM object.

        Raises:
            InvalidStateTransitionException: If the status change is not allowed.
            ModelVersionNotFoundException: If the version doesn't exist.
        """
        db_version = await self.version_repo.get(db, id=version_id)
        if not db_version:
            raise ModelVersionNotFoundException(str(version_id))

        # Example state transition logic
        if new_status == ModelVersionStatusEnum.PRODUCTION and db_version.status != ModelVersionStatusEnum.VALIDATED:
            raise InvalidStateTransitionException(
                f"Cannot move version to '{new_status}' from '{db_version.status}'. Must be 'VALIDATED' first."
            )

        update_data = {"status": new_status.value}
        return await self.version_repo.update(db, db_obj=db_version, obj_in=update_data)