"""
Initializes the ORM models package.

This file defines the declarative base that all ORM models will inherit from,
and it imports all the model classes so they are registered with SQLAlchemy's
metadata.
"""
from sqlalchemy.orm import declarative_base

# The declarative base class is the central point for SQLAlchemy's ORM mapping.
# All ORM model classes will inherit from this Base.
Base = declarative_base()

# Import all the models, so they are registered with the Base's metadata.
# This is crucial for Alembic to detect model changes for migrations.
from .ai_model_orm import AIModelORM
from .ai_model_version_orm import AIModelVersionORM
from .deployment_orm import AIModelDeploymentORM
from .model_feedback_orm import AIModelFeedbackORM
from .validation_result_orm import AIModelValidationResultORM