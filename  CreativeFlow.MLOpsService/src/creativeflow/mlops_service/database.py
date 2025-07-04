"""
SQLAlchemy database engine and session management setup.

This module provides the necessary components to connect to the PostgreSQL
database and manage database sessions throughout the application using
FastAPI's dependency injection system.
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from creativeflow.mlops_service.core.config import get_settings

# Get database settings from the configuration
settings = get_settings()

# Create the SQLAlchemy engine.
# The 'pool_pre_ping' argument checks for "stale" connections and reconnects
# if the database connection has been lost.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker factory. This will be used to create new Session
# objects. `autocommit=False` and `autoflush=False` are standard practice
# for using SQLAlchemy sessions with web frameworks.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to provide a database session.

    This is a generator function that creates a new SQLAlchemy Session for each
    request, yields it to the endpoint function, and then ensures the session
s    is closed, even if errors occur.

    Yields:
        A new SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()