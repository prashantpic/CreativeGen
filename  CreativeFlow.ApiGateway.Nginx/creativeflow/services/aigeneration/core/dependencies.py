```python
from fastapi import Depends, HTTPException, status, Header
from typing import Annotated
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.infrastructure.database.db_config import get_db_session
from creativeflow.services.aigeneration.infrastructure.repositories.postgres_generation_request_repository import PostgresGenerationRequestRepository
from creativeflow.services.aigeneration.domain.repositories.generation_request_repository import IGenerationRequestRepository
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import rabbitmq_publisher, RabbitMQPublisher
from creativeflow.services.aigeneration.infrastructure.clients.odoo_adapter_client import OdooAdapterClient
from creativeflow.services.aigeneration.application.services.credit_service_client import CreditServiceClient
from creativeflow.services.aigeneration.application.services.notification_service_client import NotificationServiceClient
from creativeflow.services.aigeneration.application.services.orchestration_service import OrchestrationService

# --- HTTP Client Dependency ---
# This can be a single instance managed by FastAPI's lifespan events
# or created per request if needed. For this service, a single client is efficient.
_http_client = httpx.AsyncClient()

def get_http_client() -> httpx.AsyncClient:
    return _http_client

# --- Repository Dependency ---
def get_generation_request_repo(
    db_session: AsyncSession = Depends(get_db_session)
) -> IGenerationRequestRepository:
    """Provides an instance of PostgresGenerationRequestRepository."""
    return PostgresGenerationRequestRepository(db_session=db_session)

# --- Messaging Dependency ---
def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """Provides the global instance of RabbitMQPublisher."""
    return rabbitmq_publisher

# --- External Client Dependencies ---
def get_odoo_adapter_client() -> OdooAdapterClient:
    """Provides an instance of OdooAdapterClient."""
    # This can be a singleton if connection management is handled internally.
    return OdooAdapterClient()

def get_credit_service_client(
    http_client: httpx.AsyncClient = Depends(get_http_client)
) -> CreditServiceClient:
    """Provides an instance of CreditServiceClient."""
    # As per SDS, CreditServiceClient could use OdooAdapterClient or a direct HTTP API.
    # This implementation assumes it uses an HTTP API via httpx.
    return CreditServiceClient(http_client=http_client)

def get_notification_client(
    http_client: httpx.AsyncClient = Depends(get_http_client)
) -> NotificationServiceClient:
    """Provides an instance of NotificationServiceClient."""
    return NotificationServiceClient(http_client=http_client)

# --- Core Service Dependency ---
def get_orchestration_service(
    repo: IGenerationRequestRepository = Depends(get_generation_request_repo),
    publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    credit_client: CreditServiceClient = Depends(get_credit_service_client),
    notification_client: NotificationServiceClient = Depends(get_notification_client)
) -> OrchestrationService:
    """
    Injects all necessary dependencies into the OrchestrationService.
    """
    return OrchestrationService(
        repo=repo,
        rabbitmq_publisher=publisher,
        credit_service_client=credit_client,
        notification_client=notification_client
    )

# --- Security Dependency for Callbacks ---
def verify_n8n_callback_secret(
    x_callback_secret: Annotated[str, Header()]
):
    """
    Verifies a shared secret from a header to secure n8n callbacks.
    """
    if x_callback_secret != settings.N8N_CALLBACK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid callback secret"
        )
```