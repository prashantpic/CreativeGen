"""
Base repository class with common SQLAlchemy CRUD operations.

This generic repository class provides a standard interface for Create, Read,
Update, and Delete operations, reducing boilerplate code in specific
repositories.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import exc

from creativeflow.mlops_service.infrastructure.database.orm_models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic base repository with common CRUD methods.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Initializes the BaseRepository.

        Args:
            model: The SQLAlchemy ORM model class.
        """
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by its ID.

        Args:
            db: The database session.
            id: The primary key ID of the record.

        Returns:
            The ORM model instance or None if not found.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            db: The database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of ORM model instances.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            db: The database session.
            obj_in: The Pydantic schema with the creation data.

        Returns:
            The newly created ORM model instance.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing record.

        Args:
            db: The database session.
            db_obj: The existing ORM model instance to update.
            obj_in: The Pydantic schema or dict with the update data.

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

    async def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        Remove a record by its ID.

        Args:
            db: The database session.
            id: The primary key ID of the record to remove.

        Returns:
            The removed ORM model instance or None if not found.
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj