"""
Base repository class with common SQLAlchemy CRUD operations.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from creativeflow.mlops_service.infrastructure.database.orm_models.ai_model_orm import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic base class for SQLAlchemy repositories with common CRUD methods.

    This class provides a standardized set of methods for interacting with a
    database model, reducing boilerplate code in specific repository implementations.

    Attributes:
        model: The SQLAlchemy ORM model class.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initializes the BaseRepository.

        Args:
            model: The SQLAlchemy ORM model class this repository will manage.
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Retrieves a single record by its primary key.

        Args:
            db: The SQLAlchemy database session.
            id: The primary key of the record to retrieve.

        Returns:
            The ORM model instance if found, otherwise None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieves multiple records with pagination.

        Args:
            db: The SQLAlchemy database session.
            skip: The number of records to skip (for pagination).
            limit: The maximum number of records to return.

        Returns:
            A list of ORM model instances.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Creates a new record in the database.

        Args:
            db: The SQLAlchemy database session.
            obj_in: The Pydantic schema with the data for the new record.

        Returns:
            The newly created ORM model instance.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Updates an existing record in the database.

        Args:
            db: The SQLAlchemy database session.
            db_obj: The existing ORM model instance to update.
            obj_in: A Pydantic schema or dict with the fields to update.

        Returns:
            The updated ORM model instance.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        Removes a record from the database.

        Args:
            db: The SQLAlchemy database session.
            id: The primary key of the record to remove.

        Returns:
            The removed ORM model instance if found, otherwise None.
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj