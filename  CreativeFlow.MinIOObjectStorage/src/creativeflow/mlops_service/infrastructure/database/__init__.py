"""
Initializes the database infrastructure package.

This package contains all components related to database interaction,
including SQLAlchemy ORM models, repository implementations for data access,
and the base repository class.
"""
from .base_repository import BaseRepository

__all__ = ["BaseRepository"]