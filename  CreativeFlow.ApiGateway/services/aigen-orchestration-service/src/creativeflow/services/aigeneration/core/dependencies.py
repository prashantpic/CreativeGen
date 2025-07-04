import logging
from typing import AsyncGenerator

import httpx
import pika
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from creativeflow.services.aigeneration.infrastructure.database.db_config import SessionLocal, engine
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository

logger = logging.getLogger(__name__)

# Single instances of clients to reuse connections
http_client = httpx.AsyncClient()
rabbitmq_publisher_instance = RabbitMQPublisher(
    amqp_url=settings.RABBITMQ_URL,
    exchange_name=settings.RABBITMQ_GENERATION_EXCHANGE
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an SQLAlchemy AsyncSession.
    Ensures the session is closed after the request is finished.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    Provides an instance of RabbitMQPublisher.
    Connection is managed globally via startup/shutdown events.
    """
    if not rabbitmq_publisher_instance.is_connected:
        logger.warning("RabbitMQ publisher is not connected. Attempting to reconnect.")
        # In a real-world scenario, you might have more robust reconnection logic here
        # or rely on startup events. For now, we raise an error.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Message queue service is currently unavailable."
        )
    return rabbitmq_publisher_instance

def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """
    Dependency that provides an instance of the generation request repository.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)

def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    Dependency that provides an instance of the OdooAdapterClient.
    """
    # This client could be a singleton if connection management is handled internally.
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=settings.ODOO_PASSWORD
    )

def get_credit_service_client() -> CreditServiceClient:
    """
    Dependency that provides an instance of the CreditServiceClient.
    Reuses a global httpx.AsyncClient.
    """
    return CreditServiceClient(base_url=str(settings.CREDIT_SERVICE_API_URL), http_client=http_client)

def get_notification_client() -> NotificationServiceClient:
    """
    Dependency that provides an instance of the NotificationServiceClient.
    Reuses a global httpx.AsyncClient.
    """
    return NotificationServiceClient(base_url=str(settings.NOTIFICATION_SERVICE_API_URL), http_client=http_client)

def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client)
) -> OrchestrationService:
    """
    Dependency that constructs and provides an instance of the OrchestrationService
    with all its necessary dependencies.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=settings
    )

def verify_n8n_secret(x_callback_secret: str = Header(...)):
    """
    Dependency to verify the shared secret from n8n callbacks.
    """
    if x_callback_secret != settings.N8N_CALLBACK_SECRET:
        logger.warning("Invalid n8n callback secret received.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid callback secret"
        )