import logging
from typing import AsyncGenerator

import httpx
import pika
from fastapi import Depends, HTTPException, status, Header, Request
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

logger = logging.getLogger(__name__)

# Global instances for clients to be managed by startup/shutdown events
# This helps in reusing connections (e.g., HTTP connection pools, RabbitMQ connection)
# across multiple requests.
app_state = {}

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that provides an SQLAlchemy AsyncSession.
    Ensures the session is closed after the request is finished.
    """
    async with SessionLocal() as session:
        yield session

def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    Provides a singleton instance of RabbitMQPublisher from the app state.
    The instance is created during application startup.
    """
    publisher = app_state.get("rabbitmq_publisher")
    if not publisher:
        logger.error("RabbitMQ publisher not initialized. Check startup event.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Message queue service is not available."
        )
    return publisher
    
def get_httpx_client() -> httpx.AsyncClient:
    """
    Provides a singleton instance of httpx.AsyncClient from the app state.
    """
    client = app_state.get("httpx_client")
    if not client:
        logger.error("HTTPX client not initialized. Check startup event.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal HTTP client is not available."
        )
    return client

def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """
    Dependency function that returns an instance of the repository.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)

def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    Dependency function that returns an instance of the OdooAdapterClient.
    For now, it's a simple instantiation. In a real scenario, it might manage
    a connection pool or session.
    """
    # This could be a singleton if the odoorpc library supports it
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=settings.ODOO_PASSWORD,
    )

def get_credit_service_client(
    http_client: httpx.AsyncClient = Depends(get_httpx_client)
) -> CreditServiceClient:
    """
    Dependency function that returns an instance of the CreditServiceClient.
    Injects an httpx client for making requests.
    """
    return CreditServiceClient(
        base_url=str(settings.CREDIT_SERVICE_API_URL), 
        http_client=http_client
    )

def get_notification_client(
    http_client: httpx.AsyncClient = Depends(get_httpx_client)
) -> NotificationServiceClient:
    """
    Dependency function that returns an instance of the NotificationServiceClient.
    """
    return NotificationServiceClient(
        base_url=str(settings.NOTIFICATION_SERVICE_API_URL), 
        http_client=http_client
    )

def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client),
) -> OrchestrationService:
    """
    Dependency function that constructs and returns an instance of the OrchestrationService,
    injecting all its required dependencies.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=settings
    )

def verify_n8n_secret(x_n8n_secret: str = Header(...)):
    """
    Dependency to verify the shared secret from n8n callbacks.
    """
    if x_n8n_secret != settings.N8N_CALLBACK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid secret token for n8n callback.",
        )