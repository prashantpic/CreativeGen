import httpx
from typing import AsyncGenerator, Generator
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.core.config import get_settings, Settings
from creativeflow.services.aigeneration.infrastructure.database.db_config import SessionLocal, engine
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService

# Singletons for clients and publisher
# In a real-world scenario, you might manage these connections more robustly,
# for example, with a connection pool for httpx clients.
# For RabbitMQ, a singleton publisher that manages its connection is a common pattern.
http_client = httpx.AsyncClient()
rabbitmq_publisher_instance = RabbitMQPublisher(settings=get_settings())

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a SQLAlchemy AsyncSession.
    Ensures the session is closed after the request.
    """
    async with SessionLocal() as session:
        yield session

def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session),
) -> IGenerationRequestRepository:
    """
    Dependency that provides an instance of the GenerationRequest repository.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)

async def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    Dependency that provides a singleton instance of the RabbitMQPublisher.
    The connection is managed within the publisher instance itself (see main.py startup/shutdown).
    """
    return rabbitmq_publisher_instance

def get_odoo_adapter_client(
    settings: Settings = Depends(get_settings),
) -> OdooAdapterClient:
    """
    Dependency that provides an instance of the OdooAdapterClient.
    """
    # This could be a singleton if connection setup is expensive
    return OdooAdapterClient(settings=settings)

def get_credit_service_client(
    settings: Settings = Depends(get_settings),
) -> CreditServiceClient:
    """
    Dependency that provides an instance of the CreditServiceClient.
    It uses a shared httpx.AsyncClient instance.
    """
    return CreditServiceClient(http_client=http_client, settings=settings)

def get_notification_client(
    settings: Settings = Depends(get_settings),
) -> NotificationServiceClient:
    """
    Dependency that provides an instance of the NotificationServiceClient.
    It uses a shared httpx.AsyncClient instance.
    """
    return NotificationServiceClient(http_client=http_client, settings=settings)

def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client),
    settings: Settings = Depends(get_settings),
) -> OrchestrationService:
    """
    Dependency that constructs and provides an instance of the OrchestrationService,
    injecting all its required dependencies.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=settings,
    )

def verify_n8n_secret(
    x_n8n_secret: str = Header(...),
    settings: Settings = Depends(get_settings)
):
    """
    Dependency to verify the shared secret from n8n callbacks.
    """
    if x_n8n_secret != settings.N8N_CALLBACK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid secret for n8n callback"
        )