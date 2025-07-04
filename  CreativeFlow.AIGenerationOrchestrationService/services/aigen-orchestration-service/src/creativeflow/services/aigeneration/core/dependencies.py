"""
Defines FastAPI dependencies for dependency injection.

This module provides functions for injecting shared resources such as database sessions,
service clients, and repository instances into FastAPI path operation functions.
This follows the dependency injection pattern to promote loose coupling and testability.
"""

from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.core.config import Settings, settings
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.database.db_config import SessionLocal
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient

# This global instance will be managed by startup/shutdown events in main.py
# to ensure connections are handled gracefully.
rabbitmq_publisher_instance: Optional[RabbitMQPublisher] = None


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide an SQLAlchemy AsyncSession.

    Yields a database session from the session factory and ensures it's closed
    after the request is processed.
    """
    async with SessionLocal() as session:
        yield session


async def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    FastAPI dependency that provides a singleton RabbitMQPublisher instance.

    The instance is managed globally and initialized at application startup.
    This prevents creating new connections for every request.
    """
    if rabbitmq_publisher_instance is None:
        # This state should not be reached in a running application as the
        # instance is created on startup. This is a safeguard.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RabbitMQ publisher is not available.",
        )
    return rabbitmq_publisher_instance


def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session),
) -> IGenerationRequestRepository:
    """
    FastAPI dependency that provides a GenerationRequestRepository instance.

    Injects an async database session into the repository implementation.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)


def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    FastAPI dependency that provides an OdooAdapterClient instance.
    The client is configured from application settings.
    """
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=str(settings.ODOO_PASSWORD), # Ensure password is a string
    )


def get_credit_service_client() -> CreditServiceClient:
    """
    FastAPI dependency that provides a CreditServiceClient instance.
    This client interacts with the dedicated Credit Service API via HTTP.
    """
    # Assumes CreditServiceClient is stateless and uses httpx.AsyncClient internally.
    # A single client instance can be reused across the application via `Depends`.
    return CreditServiceClient(base_url=settings.CREDIT_SERVICE_API_URL)


def get_notification_client() -> NotificationServiceClient:
    """
    FastAPI dependency that provides a NotificationServiceClient instance.
    """
    return NotificationServiceClient(base_url=settings.NOTIFICATION_SERVICE_API_URL)


def get_settings() -> Settings:
    """
    FastAPI dependency to provide the application settings object.
    """
    return settings


def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client),
    app_settings: Settings = Depends(get_settings),
) -> OrchestrationService:
    """
    FastAPI dependency that constructs and provides the core OrchestrationService.

    Injects all necessary dependencies (repository, message publisher, service clients, settings)
    into the service, making it ready to handle business logic.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=app_settings,
    )