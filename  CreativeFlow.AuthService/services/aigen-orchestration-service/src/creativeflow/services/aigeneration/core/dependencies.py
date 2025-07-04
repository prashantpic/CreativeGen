from typing import AsyncGenerator

import httpx
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from creativeflow.services.aigeneration.infrastructure.database.db_config import SessionLocal
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository


# Database Dependency
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an SQLAlchemy AsyncSession from SessionLocal.
    Ensures the session is closed after the request.
    """
    async with SessionLocal() as session:
        yield session

# Infrastructure Dependencies
async def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """
    Provides a singleton instance of RabbitMQPublisher.
    Connection is managed globally in main.py startup/shutdown events.
    """
    return RabbitMQPublisher.get_instance()

def get_generation_request_repo(db_session: AsyncSession = Depends(get_db_session)) -> IGenerationRequestRepository:
    """
    Returns an instance of PostgresGenerationRequestRepository initialized with a DB session.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)

def get_odoo_adapter_client() -> OdooAdapterClient:
    """
    Returns an instance of OdooAdapterClient.
    """
    return OdooAdapterClient(
        url=settings.ODOO_URL,
        db=settings.ODOO_DB,
        uid=settings.ODOO_UID,
        password=settings.ODOO_PASSWORD,
    )

# Service Client Dependencies
def get_credit_service_client() -> CreditServiceClient:
    """
    Returns an instance of CreditServiceClient.
    """
    # NOTE: This client could internally use the OdooAdapterClient if Odoo is the source of truth
    # and there's no separate credit service API. For this implementation, we assume a dedicated API.
    return CreditServiceClient(
        base_url=settings.CREDIT_SERVICE_API_URL,
        http_client=httpx.AsyncClient()
    )

def get_notification_client() -> NotificationServiceClient:
    """
    Returns an instance of NotificationServiceClient.
    """
    return NotificationServiceClient(
        base_url=settings.NOTIFICATION_SERVICE_API_URL,
        http_client=httpx.AsyncClient()
    )

# Application Service Dependency
def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client)
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
def verify_n8n_secret(x_callback_secret: str = Header(...)):
    """
    Verifies the shared secret for n8n callbacks.
    """
    if x_callback_secret != settings.N8N_CALLBACK_SHARED_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid callback secret"
        )