"""
SQLAlchemy database engine and session management setup.

This module configures the SQLAlchemy database engine, session factory, and
a dependency-injectable function `get_db` for use in FastAPI routes.
This provides a consistent way to access database sessions throughout the application.
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from creativeflow.mlops_service.core.config import get_settings

# Load application settings
settings = get_settings()

# Create the SQLAlchemy engine
# The `pool_pre_ping` argument helps in preventing issues with stale database connections.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker instance
# This is a factory for creating new Session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """

    FastAPI dependency to get a database session.

    This function is a generator that yields a new SQLAlchemy Session for each
    request, and ensures it's closed after the request is finished, even if
    an error occurs.

    Yields:
        Session: A new SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()