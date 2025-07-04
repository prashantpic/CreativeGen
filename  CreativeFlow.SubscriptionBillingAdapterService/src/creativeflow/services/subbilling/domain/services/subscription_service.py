import logging
from uuid import UUID
from typing import Optional

from ..models.subscription_models import UserSubscriptionDomain, FreemiumLimits
from ...infrastructure.odoo_client import OdooClient
from ...infrastructure.db.repositories.user_repository import UserRepository
from .odoo_mapping_service import OdooMappingService
from ...infrastructure.odoo_client import OdooRPCError

logger = logging.getLogger(__name__)

class SubscriptionService:
    """
    Contains the business logic for managing user subscriptions.
    It orchestrates calls to Odoo and uses the user repository for context.
    """

    def __init__(
        self,
        odoo_client: OdooClient,
        user_repo: UserRepository,
        odoo_map_service: OdooMappingService,
    ):
        self.odoo_client = odoo_client
        self.user_repo = user_repo
        self.odoo_map_service = odoo_map_service

    async def get_user_subscription_status(self, user_id: UUID) -> UserSubscriptionDomain:
        """
        Retrieves a user's full subscription status, including plan features and limits.
        """
        logger.info(f"Fetching subscription status for user {user_id}")
        
        try:
            odoo_subscription_data = self.odoo_client.get_current_user_plan_info(str(user_id))
            
            # Map the raw Odoo response to our internal domain model
            user_subscription = self.odoo_map_service.from_odoo_subscription_to_domain(
                user_id=user_id,
                odoo_data=odoo_subscription_data
            )
            
            # If on a free plan, fetch freemium usage details
            if user_subscription.freemium_limits:
                # This conceptual call would get usage from Odoo
                # usage_count = self.odoo_client.get_freemium_usage_count(str(user_id))
                # user_subscription.freemium_limits.generations_used_this_month = usage_count
                pass # Placeholder for actual usage fetching logic
            
            return user_subscription
        except OdooRPCError as e:
            logger.error(f"Odoo RPC Error fetching subscription for user {user_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching subscription for user {user_id}: {e}", exc_info=True)
            raise


    async def process_subscription_change(self, user_id: UUID, new_plan_id: str, action: str) -> UserSubscriptionDomain:
        """
        Processes a subscription change (upgrade, downgrade, cancel) by calling Odoo.
        """
        logger.info(f"Processing subscription change for user {user_id}: action='{action}', new_plan_id='{new_plan_id}'")
        
        # In a real scenario, we'd map our internal `new_plan_id` (e.g., 'pro_monthly')
        # to an Odoo `product.product` ID. This could be a static map or another Odoo call.
        # For this example, we'll assume a direct mapping or that `new_plan_id` is the Odoo ID.
        try:
            new_plan_odoo_id = int(new_plan_id) # Simplistic assumption
        except ValueError:
             raise ValueError("Invalid new_plan_id format. Expected Odoo product ID.")

        try:
            self.odoo_client.update_subscription(str(user_id), new_plan_odoo_id, action)
            logger.info(f"Successfully processed subscription change in Odoo for user {user_id}")
            
            # After a successful change, fetch the new state and return it.
            return await self.get_user_subscription_status(user_id)
        except OdooRPCError as e:
            logger.error(f"Odoo RPC Error changing subscription for user {user_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error changing subscription for user {user_id}: {e}", exc_info=True)
            raise

    async def check_feature_access(self, user_id: UUID, feature_key: str) -> bool:
        """
        Checks if a user has access to a specific feature based on their subscription.
        """
        logger.debug(f"Checking feature '{feature_key}' access for user {user_id}")
        subscription = await self.get_user_subscription_status(user_id)
        
        if not hasattr(subscription.features, feature_key):
            logger.warning(f"Attempted to check non-existent feature '{feature_key}'")
            return False
            
        has_access = getattr(subscription.features, feature_key, False)
        logger.debug(f"User {user_id} access to '{feature_key}': {has_access}")
        return has_access

    async def get_freemium_usage(self, user_id: UUID) -> FreemiumLimits:
        """
        Retrieves the current freemium usage and limits for a user.
        """
        logger.info(f"Fetching freemium usage for user {user_id}")
        subscription = await self.get_user_subscription_status(user_id)
        
        if not subscription.freemium_limits:
            # This can happen if the user is on a paid plan.
            # We return a default object indicating no limits apply in this context.
            return FreemiumLimits(generations_used_this_month=0, monthly_generations_limit=0)
            
        return subscription.freemium_limits