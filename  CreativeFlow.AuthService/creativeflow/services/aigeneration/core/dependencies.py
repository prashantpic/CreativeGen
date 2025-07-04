import logging
from typing import AsyncGenerator

import httpx
from fastapi import Depends, HTTPException, status, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
import aio_pika

from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from creativeflow.services.aigeneration.infrastructure.database.db_config import SessionLocal, engine
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import \
    PostgresGenerationRequestRepository

logger = logging.getLogger(__name__)

# --- Database Dependencies ---
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an SQLAlchemy AsyncSession for a request.
    """
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rollback due to exception: {e}")
            raise
        finally:
            await session.close()


def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """
    Dependency that provides an instance of the GenerationRequest repository.
    """
    return PostgresGenerationRequestRepository(db_session)


# --- Messaging Dependencies ---
def get_rabbitmq_publisher(request: Request) -> RabbitMQPublisher:
    """
    Provides the singleton instance of RabbitMQPublisher from the app state.
    """
    return request.app.state.rabbitmq_publisher


# --- External Service Client Dependencies ---
# Singleton client instances
_httpx_client = httpx.AsyncClient()

def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    Dependency that provides an instance of OdooAdapterClient.
    """
    # This could be a singleton if connection setup is expensive
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=settings.ODOO_PASSWORD
    )

def get_credit_service_client() -> CreditServiceClient:
    """
    Dependency that provides an instance of CreditServiceClient.
    Using a shared httpx client instance.
    """
    return CreditServiceClient(
        http_client=_httpx_client,
        base_url=settings.CREDIT_SERVICE_API_URL
    )

def get_notification_client() -> NotificationServiceClient:
    """
    Dependency that provides an instance of NotificationServiceClient.
    Using a shared httpx client instance.
    """
    return NotificationServiceClient(
        http_client=_httpx_client,
        base_url=settings.NOTIFICATION_SERVICE_API_URL
    )


# --- Core Application Service Dependency ---
def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client)
) -> OrchestrationService:
    """
    Dependency that provides an instance of the core OrchestrationService,
    injecting all its required dependencies.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client
    )

# --- Security Dependencies ---
def verify_n8n_secret(x_callback_secret: str = Header(...)):
    """
    Dependency to verify the shared secret from n8n callbacks.
    """
    if x_callback_secret != settings.N8N_CALLBACK_SECRET:
        logger.warning("Invalid n8n callback secret received.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid callback secret."
        )