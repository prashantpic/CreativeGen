from typing import Optional, Generator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session as SQLAlchemySession

from .core.config import Settings, settings
from .infrastructure.odoo_client import OdooClient
from .infrastructure.stripe_client import StripeClient
from .infrastructure.paypal_client import PayPalClient
from .infrastructure.db.database import get_db
from .infrastructure.db.repositories.user_repository import UserRepository
from .domain.services.subscription_service import SubscriptionService
from .domain.services.credit_service import CreditService
from .domain.services.payment_orchestration_service import PaymentOrchestrationService
from .domain.services.odoo_mapping_service import OdooMappingService

# Using lru_cache(maxsize=1) is a simple way to create a singleton instance
# for the duration of the application's lifecycle.

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return settings

@lru_cache(maxsize=1)
def get_odoo_client(settings_dep: Settings = Depends(get_settings)) -> OdooClient:
    return OdooClient(config=settings_dep)

@lru_cache(maxsize=1)
def get_stripe_client(settings_dep: Settings = Depends(get_settings)) -> Optional[StripeClient]:
    if settings_dep.ENABLE_DIRECT_STRIPE_CALLS and settings_dep.STRIPE_API_KEY:
        return StripeClient(api_key=settings_dep.STRIPE_API_KEY.get_secret_value())
    return None

@lru_cache(maxsize=1)
def get_paypal_client(settings_dep: Settings = Depends(get_settings)) -> Optional[PayPalClient]:
    if settings_dep.ENABLE_DIRECT_PAYPAL_CALLS and settings_dep.PAYPAL_CLIENT_ID and settings_dep.PAYPAL_CLIENT_SECRET:
        return PayPalClient(
            client_id=settings_dep.PAYPAL_CLIENT_ID.get_secret_value(),
            client_secret=settings_dep.PAYPAL_CLIENT_SECRET.get_secret_value()
        )
    return None

@lru_cache(maxsize=1)
def get_odoo_mapping_service() -> OdooMappingService:
    return OdooMappingService()

# --- Repository Providers ---
# Repositories are typically instantiated per request because they are tied to a DB session.

def get_user_repository(db: SQLAlchemySession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)

# --- Service Providers ---
# Services can be singletons if they are stateless, or per-request if they hold state.
# Here we make them singletons by depending on singleton clients.

@lru_cache(maxsize=1)
def get_subscription_service(
    odoo_client: OdooClient = Depends(get_odoo_client),
    user_repo: UserRepository = Depends(get_user_repository),
    odoo_map_service: OdooMappingService = Depends(get_odoo_mapping_service)
) -> SubscriptionService:
    return SubscriptionService(
        odoo_client=odoo_client,
        user_repo=user_repo,
        odoo_map_service=odoo_map_service
    )

@lru_cache(maxsize=1)
def get_credit_service(
    odoo_client: OdooClient = Depends(get_odoo_client),
    user_repo: UserRepository = Depends(get_user_repository),
    odoo_map_service: OdooMappingService = Depends(get_odoo_mapping_service),
    subscription_service: SubscriptionService = Depends(get_subscription_service) # Credit service needs sub service
) -> CreditService:
    return CreditService(
        odoo_client=odoo_client,
        user_repo=user_repo,
        odoo_map_service=odoo_map_service,
        subscription_service=subscription_service
    )

@lru_cache(maxsize=1)
def get_payment_orchestration_service(
    odoo_client: OdooClient = Depends(get_odoo_client),
    user_repo: UserRepository = Depends(get_user_repository),
    odoo_map_service: OdooMappingService = Depends(get_odoo_mapping_service),
    stripe_client: Optional[StripeClient] = Depends(get_stripe_client),
    paypal_client: Optional[PayPalClient] = Depends(get_paypal_client)
) -> PaymentOrchestrationService:
    return PaymentOrchestrationService(
        odoo_client=odoo_client,
        user_repo=user_repo,
        odoo_map_service=odoo_map_service,
        stripe_client=stripe_client,
        paypal_client=paypal_client
    )