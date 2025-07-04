import httpx
import pika
from functools import lru_cache
from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from ..application.services.orchestration_service import OrchestrationService
from ..application.services.credit_service_client import CreditServiceClient
from ..application.services.notification_service_client import NotificationServiceClient
from ..domain.repositories.generation_request_repository import IGenerationRequestRepository
from ..infrastructure.database.db_config import SessionLocal, get_db
from ..infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from ..infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository
from ..infrastructure.clients.odoo_adapter_client import OdooAdapterClient


@lru_cache()
def get_settings() -> Settings:
    return Settings()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an SQLAlchemy AsyncSession.
    Ensures the session is closed after the request.
    """
    async with SessionLocal() as session:
        yield session

def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    Provides a singleton instance of the RabbitMQPublisher.
    Connection management is handled within the publisher class.
    """
    # In a real app, you might manage this as a singleton on the app state
    # to handle connections more gracefully on startup/shutdown.
    return RabbitMQPublisher(rabbitmq_url=settings.RABBITMQ_URL)

# Repository Dependency
def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """
    Provides an instance of the PostgresGenerationRequestRepository.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)

# External Client Dependencies
@lru_cache
def get_httpx_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()

def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    Provides an instance of the OdooAdapterClient.
    """
    if not all([settings.ODOO_URL, settings.ODOO_DB, settings.ODOO_UID, settings.ODOO_PASSWORD]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Odoo settings are not configured."
        )
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=settings.ODOO_PASSWORD,
    )

def get_credit_service_client(
    client: httpx.AsyncClient = Depends(get_httpx_client)
) -> CreditServiceClient:
    """
    Provides an instance of the CreditServiceClient.
    """
    # Note: Depending on the architecture, this client might internally use
    # the OdooAdapterClient instead of a separate HTTP service.
    # The current design assumes a dedicated microservice for credits.
    return CreditServiceClient(base_url=str(settings.CREDIT_SERVICE_API_URL), http_client=client)

def get_notification_client(
    client: httpx.AsyncClient = Depends(get_httpx_client)
) -> NotificationServiceClient:
    """
    Provides an instance of the NotificationServiceClient.
    """
    return NotificationServiceClient(base_url=str(settings.NOTIFICATION_SERVICE_API_URL), http_client=client)

# Core Application Service Dependency
def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client),
) -> OrchestrationService:
    """
    Injects all necessary dependencies into the OrchestrationService.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=settings
    )

# Security Dependencies
async def verify_n8n_secret(x_callback_secret: str = Header(...)):
    """
    Verifies the shared secret provided in n8n callback headers.
    """
    if x_callback_secret != settings.N8N_CALLBACK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid callback secret."
        )