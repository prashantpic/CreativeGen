"""
FastAPI Dependencies for Dependency Injection.

This module defines functions that act as FastAPI dependencies, providing
resources like database sessions, service clients, repositories, and the
main orchestration service to the API endpoints. This follows the dependency
inversion principle and makes the application more modular and testable.
"""

import logging
from typing import AsyncGenerator

import httpx
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from ..application.services.credit_service_client import CreditServiceClient, InsufficientCreditsError, CreditServiceError
from ..application.services.notification_service_client import NotificationServiceClient
from ..application.services.orchestration_service import OrchestrationService
from ..domain.repositories.generation_request_repository import IGenerationRequestRepository
from ..infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from ..infrastructure.database.db_config import get_db_session as get_session
from ..infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from ..infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository

logger = logging.getLogger(__name__)

# --- Reusable Clients ---
# These can be managed as singletons for the application's lifecycle
# to reuse connections.
http_client_instance = httpx.AsyncClient()
rabbitmq_publisher_instance = RabbitMQPublisher(
    amqp_url=settings.RABBITMQ_URL,
    exchange_name=settings.RABBITMQ_GENERATION_EXCHANGE
)

# --- Dependency Functions ---

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an SQLAlchemy AsyncSession per request.
    It ensures the session is properly closed after the request is handled.
    """
    async with get_session() as session:
        yield session

async def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    Provides a singleton instance of the RabbitMQPublisher.
    Connection is managed globally within the publisher instance.
    """
    if not rabbitmq_publisher_instance.is_connected:
        try:
            await rabbitmq_publisher_instance.connect()
        except Exception as e:
            logger.critical(f"Failed to connect to RabbitMQ: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Messaging service is currently unavailable.",
            )
    return rabbitmq_publisher_instance

def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """
    Provides an instance of PostgresGenerationRequestRepository initialized with a DB session.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)

def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    Provides an instance of OdooAdapterClient.
    Note: This is provided as an example; direct Odoo calls might be abstracted
    away by a dedicated service like the CreditServiceClient.
    """
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=settings.ODOO_PASSWORD
    )

def get_credit_service_client() -> CreditServiceClient:
    """
    Provides an instance of CreditServiceClient.
    This client uses httpx to communicate with the dedicated credit service API.
    """
    return CreditServiceClient(
        http_client=http_client_instance,
        base_url=settings.CREDIT_SERVICE_API_URL
    )

def get_notification_client() -> NotificationServiceClient:
    """
    Provides an instance of NotificationServiceClient.
    """
    return NotificationServiceClient(
        http_client=http_client_instance,
        base_url=settings.NOTIFICATION_SERVICE_API_URL
    )

def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client)
) -> OrchestrationService:
    """
    Injects all necessary dependencies into the OrchestrationService and provides an instance.
    This is the primary dependency for the API endpoints that handle business logic.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=settings
    )

async def verify_n8n_callback_secret(
    x_callback_secret: str | None = Header(None)
) -> None:
    """
    Security dependency for n8n callback endpoints.
    Verifies that the request includes the correct shared secret in the header.
    """
    if not x_callback_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Callback secret header is missing"
        )
    if x_callback_secret != settings.N8N_CALLBACK_SHARED_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid callback secret"
        )