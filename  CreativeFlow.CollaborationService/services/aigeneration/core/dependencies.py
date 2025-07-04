from typing import AsyncGenerator, Optional
from functools import lru_cache

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.infrastructure.database.db_config import SessionLocal, get_db_session
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient, get_credit_service_client
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient, get_notification_service_client
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService

# Singletons for clients and publisher to manage connections efficiently
@lru_cache()
def get_settings() -> Settings:
    return settings

# RabbitMQ Publisher
# The publisher object will be managed by startup/shutdown events in main.py
# This dependency function just retrieves it from the app's state.
def get_rabbitmq_publisher(request: Request) -> RabbitMQPublisher:
    return request.app.state.rabbitmq_publisher

# Repositories
def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """
    Dependency to get an instance of the GenerationRequest repository.
    """
    return PostgresGenerationRequestRepository(db_session=db_session)

# External Service Clients
@lru_cache()
def get_odoo_adapter_client_instance() -> OdooAdapterClient:
    """
    Dependency to get a singleton instance of the OdooAdapterClient.
    """
    return OdooAdapterClient(
        odoo_url=settings.ODOO_URL,
        odoo_db=settings.ODOO_DB,
        odoo_uid=settings.ODOO_UID,
        odoo_password=settings.ODOO_PASSWORD,
    )

# Orchestration Service
def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    rabbitmq_publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_service_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_service_client),
    app_settings: Settings = Depends(get_settings),
) -> OrchestrationService:
    """
    Dependency to get an instance of the main OrchestrationService.
    This injects all other necessary dependencies into the service.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=rabbitmq_publisher,
        credit_service_client=credit_service_client,
        notification_client=notification_client,
        settings=app_settings,
    )

# Security
async def verify_n8n_callback_secret(request: Request, app_settings: Settings = Depends(get_settings)):
    """
    Verifies the shared secret in the callback header from n8n.
    """
    callback_secret = request.headers.get("X-Callback-Secret")
    if not callback_secret or callback_secret != app_settings.N8N_CALLBACK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing callback secret."
        )
    return True