from typing import AsyncGenerator, Annotated

import httpx
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from creativeflow.services.aigeneration.infrastructure.database.db_config import SessionLocal
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import \
    PostgresGenerationRequestRepository

# --- Global instances for clients and publishers to manage connections ---
# These will be initialized during the application's lifespan
rabbitmq_publisher_instance: RabbitMQPublisher | None = None
http_client_instance: httpx.AsyncClient | None = None


# --- Database Dependencies ---
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an SQLAlchemy AsyncSession for a request.
    Ensures the session is closed after the request is complete.
    """
    async with SessionLocal() as session:
        yield session

# --- Repository Dependencies ---
def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """
    Dependency that provides an instance of the PostgresGenerationRequestRepository.
    """
    return PostgresGenerationRequestRepository(db_session)

# --- Messaging Dependencies ---
def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    Dependency that provides a RabbitMQPublisher instance.
    The instance is managed globally and initialized on startup.
    """
    if rabbitmq_publisher_instance is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RabbitMQ publisher is not available.",
        )
    return rabbitmq_publisher_instance

# --- HTTP Client Dependencies ---
def get_http_client() -> httpx.AsyncClient:
    """
    Provides a shared httpx.AsyncClient instance.
    """
    if http_client_instance is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="HTTP Client is not available.",
        )
    return http_client_instance

# --- External Service Client Dependencies ---
def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    Provides an instance of the OdooAdapterClient.
    """
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=settings.ODOO_PASSWORD,
    )

def get_credit_service_client(
    http_client: httpx.AsyncClient = Depends(get_http_client)
) -> CreditServiceClient:
    """
    Provides an instance of the CreditServiceClient.
    """
    return CreditServiceClient(base_url=settings.CREDIT_SERVICE_API_URL, http_client=http_client)

def get_notification_client(
    http_client: httpx.AsyncClient = Depends(get_http_client)
) -> NotificationServiceClient:
    """
    Provides an instance of the NotificationServiceClient.
    """
    return NotificationServiceClient(base_url=settings.NOTIFICATION_SERVICE_API_URL, http_client=http_client)

# --- Core Application Service Dependency ---
def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client)
) -> OrchestrationService:
    """
    Dependency that constructs and provides the main OrchestrationService
    with all its required dependencies.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=settings
    )

# --- Security Dependencies ---
def verify_n8n_secret(x_callback_secret: Annotated[str | None, Header()] = None):
    """
    Verifies the shared secret for n8n callbacks.
    """
    if not x_callback_secret or x_callback_secret != settings.N8N_CALLBACK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing callback secret."
        )