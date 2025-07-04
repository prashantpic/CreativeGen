from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from ...core.config import settings

# Construct the database URL from settings, retrieving the secret value.
# The format should be, e.g., "postgresql+psycopg2://user:password@host:port/dbname"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.get_secret_value()

# Create the SQLAlchemy engine. `pool_pre_ping` is good practice for resiliency.
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create a session factory. This will be used to create new Session objects.
# `autocommit=False` and `autoflush=False` are standard for FastAPI usage,
# giving explicit control over transaction boundaries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[SQLAlchemySession, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy database session.
    
    This function creates a new session for each request, handles its lifecycle,
    and ensures it's closed after the request is complete, returning the
    connection to the pool.

    Yields:
        A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()