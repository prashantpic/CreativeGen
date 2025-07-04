"""
SQLAlchemy repository for AIModel entities.

This class provides data access methods specific to AIModel entities,
inheriting common CRUD operations from the BaseRepository.
"""
from typing import Optional

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.model_schemas import (
    ModelCreateSchema, ModelUpdateSchema
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository
)
from creativeflow.mlops_service.infrastructure.database.orm_models.ai_model_orm import (
    AIModelORM
)


class ModelRepository(BaseRepository[AIModelORM, ModelCreateSchema, ModelUpdateSchema]):
    """
    Repository for managing AIModel data in PostgreSQL.
    """
    async def get_by_name(self, db: Session, *, name: str) -> Optional[AIModelORM]:
        """
        Get an AI model by its unique name.

        Args:
            db: The database session.
            name: The name of the model.

        Returns:
            The AIModelORM instance or None if not found.
        """
        return db.query(AIModelORM).filter(AIModelORM.name == name).first()

# Instantiate the repository
model_repository = ModelRepository(AIModelORM)