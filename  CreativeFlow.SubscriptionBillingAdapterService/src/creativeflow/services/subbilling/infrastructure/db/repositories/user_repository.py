import uuid
from typing import Optional

from sqlalchemy.orm import Session as SQLAlchemySession
from .. import models_db

class UserRepository:
    """
    Repository for accessing User data context from the PostgreSQL database.
    This class abstracts database queries for the User model projection.
    It is intended for read-only operations within this service.
    """
    def __init__(self, db: SQLAlchemySession):
        """
        Initializes the repository with a database session.
        Args:
            db: An active SQLAlchemy session.
        """
        self.db = db

    def get_user_context_by_id(self, user_id: uuid.UUID) -> Optional[models_db.User]:
        """
        Retrieves a user's context by their platform UUID.
        
        Args:
            user_id: The UUID of the user.
        
        Returns:
            The User ORM model instance if found, otherwise None.
        """
        return self.db.query(models_db.User).filter(models_db.User.id == user_id).first()

    def get_user_by_odoo_partner_id(self, odoo_partner_id: int) -> Optional[models_db.User]:
        """
        Retrieves a user's context by their Odoo Partner ID.
        This can be useful for reverse lookups (e.g., from an Odoo webhook).
        
        Args:
            odoo_partner_id: The integer ID of the res.partner in Odoo.
        
        Returns:
            The User ORM model instance if found, otherwise None.
        """
        return self.db.query(models_db.User).filter(models_db.User.odoo_partner_id == odoo_partner_id).first()

    def get_odoo_partner_id(self, user_id: uuid.UUID) -> Optional[int]:
        """
        A convenience method to directly fetch the Odoo Partner ID for a given user UUID.
        
        Args:
            user_id: The UUID of the user.
            
        Returns:
            The integer Odoo Partner ID if the user and the ID exist, otherwise None.
        """
        user = self.get_user_context_by_id(user_id)
        return user.odoo_partner_id if user else None