import logging
from uuid import UUID
from typing import Optional, Dict, List

from ...core.config import settings
from ...infrastructure.odoo_client import OdooClient, OdooRPCError
from ...infrastructure.stripe_client import StripeClient
from ...infrastructure.paypal_client import PayPalClient
from ...infrastructure.db.repositories.user_repository import UserRepository
from .odoo_mapping_service import OdooMappingService

logger = logging.getLogger(__name__)

class PaymentOrchestrationService:
    """
    Orchestrates payment, invoicing, and tax operations, primarily by delegating to Odoo.
    It can also interact directly with payment gateways for specific, limited use cases.
    """

    def __init__(
        self,
        odoo_client: OdooClient,
        user_repo: UserRepository,
        odoo_map_service: OdooMappingService,
        stripe_client: Optional[StripeClient],
        paypal_client: Optional[PayPalClient],
    ):
        self.odoo_client = odoo_client
        self.user_repo = user_repo
        self.odoo_map_service = odoo_map_service
        self.stripe_client = stripe_client
        self.paypal_client = paypal_client

    async def get_user_invoices_portal_url(self, user_id: UUID) -> Optional[str]:
        """
        Gets a link to the user's portal page in Odoo where they can view invoices.
        """
        logger.info(f"Getting invoice portal URL for user {user_id}")
        return self.odoo_client.get_payment_portal_link_for_user(str(user_id))

    async def list_user_invoices(self, user_id: UUID, limit: int) -> List[Dict]:
        """Retrieves a list of invoices for a user from Odoo."""
        logger.info(f"Listing invoices for user {user_id} with limit {limit}")
        try:
            raw_invoices = self.odoo_client.get_invoices_for_user(str(user_id), limit)
            return [self.odoo_map_service.from_odoo_invoice_to_summary(inv) for inv in raw_invoices]
        except OdooRPCError as e:
            logger.error(f"Odoo error listing invoices for user {user_id}: {e}")
            return []

    async def get_payment_method_update_url(self, user_id: UUID, provider: str, return_url: str) -> Optional[str]:
        """
        Gets a URL for the user to update their payment method.
        This can be a direct link to the provider (Stripe) or a link to the Odoo portal.
        """
        logger.info(f"Getting payment method update URL for user {user_id}, provider '{provider}'")
        
        if provider == "stripe" and settings.ENABLE_DIRECT_STRIPE_CALLS and self.stripe_client:
            # For Stripe, we can generate a direct Billing Portal link if enabled.
            # This requires fetching the stripe_customer_id from Odoo.
            # Conceptual: odoo_client needs a method to get this.
            # stripe_cust_id = self.odoo_client.get_stripe_customer_id(str(user_id))
            stripe_cust_id = "cus_placeholder" # Placeholder
            if stripe_cust_id:
                return self.stripe_client.get_payment_method_update_session_url(stripe_cust_id, return_url)

        if provider == "paypal" and settings.ENABLE_DIRECT_PAYPAL_CALLS and self.paypal_client:
            # For PayPal, we can try to get a link if the client supports it.
            # paypal_sub_id = self.odoo_client.get_paypal_subscription_id(str(user_id))
            paypal_sub_id = "I-placeholder" # Placeholder
            if paypal_sub_id:
                return self.paypal_client.get_payment_method_update_portal_url(paypal_sub_id)

        # Fallback for any other provider or if direct calls are disabled.
        # The Odoo portal is the generic place to manage subscriptions and payment methods.
        logger.info(f"Falling back to Odoo portal URL for payment management for user {user_id}")
        return self.odoo_client.get_payment_portal_link_for_user(str(user_id))
    
    async def get_tax_information_for_purchase(self, user_id: UUID, purchase_details: Dict) -> Dict:
        """
        Gets calculated tax information for a potential purchase by calling Odoo's tax engine.
        """
        logger.info(f"Calculating tax for purchase preview for user {user_id}")
        # The purchase_details from the API need to be mapped to what Odoo expects.
        # This might involve product IDs, quantities, and partner shipping address from Odoo.
        odoo_order_details = self.odoo_map_service.to_odoo_tax_calc_details(user_id, purchase_details)
        try:
            tax_info = self.odoo_client.calculate_tax_for_order(odoo_order_details)
            return self.odoo_map_service.from_odoo_tax_calc_to_domain(tax_info)
        except OdooRPCError as e:
            logger.error(f"Odoo error calculating tax for user {user_id}: {e}")
            raise
    
    async def handle_failed_payment(self, user_id: UUID, odoo_subscription_id: int, failure_reason: str):
        """
        Notifies Odoo about a failed payment to trigger dunning processes.
        """
        logger.warning(f"Handling failed payment for user {user_id}, subscription {odoo_subscription_id}. Reason: {failure_reason}")
        try:
            self.odoo_client.process_dunning_notification(odoo_subscription_id, failure_reason)
        except OdooRPCError as e:
            logger.error(f"Odoo error processing dunning for subscription {odoo_subscription_id}: {e}")
            # Even if this fails, we log the error. The system should be resilient.