"""
Handles the dependency injection setup for the application.

This file centralizes the creation of dependency instances (repositories, services,
use cases) that will be injected into the API endpoints. It cleanly separates
the composition root from the application and infrastructure logic.
"""

from typing import Annotated

import httpx
from aio_pika.abc import AbstractRobustConnection
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ...app.interfaces import (ICreditService, IGenerationRepository,
                               IJobPublisher, INotificationService)
from ...app.use_cases.initiate_generation import InitiateGenerationUseCase
from ...app.use_cases.process_n8n_result import ProcessN8NResultUseCase
from ...config.settings import settings
from ...infrastructure.db.repositories.sqlalchemy_generation_repository import \
    SqlAlchemyGenerationRepository
from ...infrastructure.http_clients.notification_client import \
    HttpNotificationService
from ...infrastructure.http_clients.odoo_client import OdooCreditService
from ...infrastructure.messaging.pika_publisher import PikaJobPublisher


class AppDependencies:
    """A container for shared application dependencies like clients and connection pools."""
    _http_client: httpx.AsyncClient | None = None
    _pika_connection: AbstractRobustConnection | None = None

    @classmethod
    def set_http_client(cls, client: httpx.AsyncClient):
        cls._http_client = client

    @classmethod
    def get_http_client(cls) -> httpx.AsyncClient:
        if cls._http_client is None:
            raise RuntimeError("HTTP client is not initialized")
        return cls._http_client

    @classmethod
    def set_pika_connection(cls, conn: AbstractRobustConnection):
        cls._pika_connection = conn

    @classmethod
    def get_pika_connection(cls) -> AbstractRobustConnection:
        if cls._pika_connection is None:
            raise RuntimeError("Pika connection is not initialized")
        return cls._pika_connection

# --- Database Session ---
engine = create_async_engine(settings.DATABASE_URL, pool_size=settings.DATABASE_POOL_SIZE)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db_session() -> AsyncSession:
    """Dependency to provide a new database session per request."""
    async with AsyncSessionFactory() as session:
        async with session.begin():
            yield session


# --- Authentication Placeholder ---
async def get_user_id_from_token(request: Request) -> str:
    """
    Placeholder dependency to extract user ID from a JWT.
    In a real implementation, this would involve decoding and validating the token.
    For now, it can return a hardcoded UUID or one from a header for testing.
    """
    # This would parse the "Authorization: Bearer <token>" header
    # For now, let's assume a debug header or a fixed ID.
    user_id = request.headers.get("X-User-ID", "d290f1ee-6c54-4b01-90e6-d701748f0851")
    return user_id


# --- Repository Provider ---
def get_generation_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IGenerationRepository:
    return SqlAlchemyGenerationRepository(session)


# --- Service Providers ---
def get_credit_service() -> ICreditService:
    return OdooCreditService(AppDependencies.get_http_client(), settings.ODOO_SERVICE_URL)

def get_notification_service() -> INotificationService:
    return HttpNotificationService(AppDependencies.get_http_client(), settings.NOTIFICATION_SERVICE_URL)

def get_job_publisher() -> IJobPublisher:
    return PikaJobPublisher(AppDependencies.get_pika_connection())


# --- Use Case Providers ---
def get_initiate_generation_use_case(
    credit_service: Annotated[ICreditService, Depends(get_credit_service)],
    job_publisher: Annotated[IJobPublisher, Depends(get_job_publisher)],
    generation_repo: Annotated[IGenerationRepository, Depends(get_generation_repository)],
) -> InitiateGenerationUseCase:
    return InitiateGenerationUseCase(credit_service, job_publisher, generation_repo)

def get_process_n8n_result_use_case(
    generation_repo: Annotated[IGenerationRepository, Depends(get_generation_repository)],
    notification_service: Annotated[INotificationService, Depends(get_notification_service)],
    credit_service: Annotated[ICreditService, Depends(get_credit_service)],
) -> ProcessN8NResultUseCase:
    return ProcessN8NResultUseCase(generation_repo, notification_service, credit_service)