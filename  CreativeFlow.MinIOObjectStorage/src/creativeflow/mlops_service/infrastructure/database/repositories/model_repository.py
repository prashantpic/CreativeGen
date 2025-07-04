"""
SQLAlchemy repository for AIModel entities.
"""
from typing import Optional

from sqlalchemy.orm import Session

from creativeflow.mlops_service.api.v1.schemas.model_schemas import (
    ModelCreateSchema,
    ModelUpdateSchema,
)
from creativeflow.mlops_service.infrastructure.database.base_repository import (
    BaseRepository,
)
from creativeflow.mlops_service.infrastructure.database.orm_models.ai_model_orm import (
    AIModelORM,
)


class ModelRepository(BaseRepository[AIModelORM, ModelCreateSchema, ModelUpdateSchema]):
    """
    Repository for managing AIModel data in PostgreSQL.

    This class inherits from BaseRepository and provides specific data access
    methods for AIModelORM entities, such as finding a model by its name.
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[AIModelORM]:
        """
        Retrieves an AI model by its unique name.

        Args:
            db: The SQLAlchemy database session.
            name: The name of the model to retrieve.

        Returns:
            The AIModelORM instance if found, otherwise None.
        """
        return db.query(self.model).filter(self.model.name == name).first()


model_repo = ModelRepository(AIModelORM)