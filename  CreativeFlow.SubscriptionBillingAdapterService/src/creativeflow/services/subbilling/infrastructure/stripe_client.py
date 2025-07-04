import logging
from typing import Optional
import stripe

logger = logging.getLogger(__name__)

class StripeClient:
    """
    A client for direct interactions with the Stripe API.

    NOTE: This client is for conditional use only. The primary payment processor
    is Odoo. This client should only be used for functionalities that Odoo cannot
    orchestrate for the frontend, such as generating client-side portal session URLs.
    Its usage must be gated by feature flags in the application configuration.
    """

    def __init__(self, api_key: Optional[str]):
        """
        Initializes the Stripe client.

        Args:
            api_key: The Stripe API secret key. If None, the client is disabled.
        """
        self.api_key = api_key
        if self.api_key:
            stripe.api_key = self.api_key
            logger.info("StripeClient initialized with an API key.")
        else:
            logger.warning("StripeClient initialized without an API key. Direct Stripe calls will be disabled.")

    def get_payment_method_update_session_url(self, customer_stripe_id: str, return_url: str) -> Optional[str]:
        """
        Generates a URL for Stripe's customer billing portal for updating payment methods.
        Requires the customer's Stripe ID, which should be stored in Odoo.

        Args:
            customer_stripe_id: The Stripe customer ID (e.g., 'cus_...').
            return_url: The URL to redirect the user to after they finish managing their details.

        Returns:
            The URL for the Stripe Billing Portal session, or None if an error occurs or
            the client is not configured.
        """
        if not self.api_key:
            logger.error("Attempted to call Stripe without an API key configured.")
            return None

        try:
            logger.info(f"Creating Stripe Billing Portal session for customer: {customer_stripe_id}")
            portal_session = stripe.billing_portal.Session.create(
                customer=customer_stripe_id,
                return_url=return_url,
            )
            return portal_session.url
        except stripe.error.StripeError as e:
            logger.error(f"Stripe API error creating billing portal session for {customer_stripe_id}: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating Stripe billing portal session: {e}", exc_info=True)
            return None

    # --- Other methods placeholder ---
    # Implement other direct Stripe interactions here ONLY IF they cannot be handled via Odoo.
    # For example:
    # def create_setup_intent(self, customer_stripe_id: str) -> Optional[dict]:
    #     """
    #     Creates a SetupIntent for collecting payment method details for future use,
    #     if this flow is managed by our frontend directly.
    #     """
    #     if not self.api_key:
    #         return None
    #     try:
    #         setup_intent = stripe.SetupIntent.create(customer=customer_stripe_id)
    #         return {"client_secret": setup_intent.client_secret}
    #     except stripe.error.StripeError as e:
    #         logger.error(f"Stripe API error creating SetupIntent for {customer_stripe_id}: {e}")
    #         return None