"""
Domain Repositories Interfaces Package

This package defines the abstract interfaces (contracts) for data persistence,
separating the domain logic from the data access layer implementation.
"""
from .publish_job_repository import IPublishJobRepository
from .social_connection_repository import ISocialConnectionRepository

__all__ = ["ISocialConnectionRepository", "IPublishJobRepository"]