import json
import logging
import pprint
import stripe

from odoo import http, _
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaymentWebhookController(http.Controller):

    @http.route('/payment/stripe/webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def stripe_webhook(self, **post):
        """
        Stripe webhook endpoint to handle asynchronous payment events.
        It verifies the webhook signature and processes events like
        'checkout.session.completed' and 'invoice.paid'.
        """
        payload = request.httprequest.data
        sig_header = request.httprequest.headers.get('Stripe-Signature')
        
        ICP = request.env['ir.config_parameter'].sudo()
        endpoint_secret = ICP.get_param('stripe.webhook.secret')

        if not endpoint_secret:
            _logger.error("Stripe webhook secret is not configured in Odoo.")
            return request.make_response("Configuration error", status=500)

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            _logger.error("Stripe webhook error: Invalid payload. %s", e)
            return request.make_response("Invalid payload", status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            _logger.error("Stripe webhook error: Invalid signature. %s", e)
            return request.make_response("Invalid signature", status=400)

        _logger.info("Stripe webhook received: %s", event.type)

        if event.type == 'checkout.session.completed':
            session = event.data.object
            self._handle_checkout_session(session)
        elif event.type == 'invoice.paid':
            invoice = event.data.object
            self._handle_invoice_paid(invoice)
        else:
            _logger.info("Stripe webhook: Unhandled event type %s", event.type)

        return request.make_response("OK", status=200)
        
    def _handle_checkout_session(self, session):
        """Process a completed Stripe Checkout session."""
        client_reference_id = session.get('client_reference_id')
        if not client_reference_id:
            _logger.warning("Stripe checkout.session.completed without client_reference_id.")
            return

        # client_reference_id should be in the format 'SO-user-ID-123' or similar
        try:
            model_name, record_id_str, user_id_str = client_reference_id.split('-')
            record_id = int(record_id_str)
            user_id = int(user_id_str)
        except (ValueError, TypeError) as e:
            _logger.error("Could not parse client_reference_id '%s': %s", client_reference_id, e)
            return
            
        user = request.env['res.users'].browse(user_id)
        if not user.exists():
            _logger.error("User with ID %s from Stripe session not found.", user_id)
            return
            
        # Example logic for a credit pack purchase
        # In a real scenario, you would look up the sale order or invoice
        # to get the exact products and quantities.
        # Here we'll just check the amount for a simplified example.
        amount_total = session.get('amount_total', 0) / 100 # Amount is in cents
        
        # A more robust implementation would check line items.
        # For simplicity, we assume one-off payments are for credits.
        # A subscription creation would be handled differently.
        if session.get('mode') == 'payment':
            # This is a one-time payment, likely for credits
            # This is a simplified logic, a real implementation would use
            # a mapping of price_id to credit amount
            credit_amount = amount_total * 10 # Example: $1 = 10 credits
            description = f"Purchase of {credit_amount} credits via Stripe Checkout"
            try:
                user.add_credits(credit_amount, description)
                _logger.info("Successfully added %s credits to user %s from Stripe session.", credit_amount, user.name)
            except UserError as e:
                _logger.error("Failed to add credits to user %s: %s", user.name, e)


    def _handle_invoice_paid(self, invoice):
        """Process a paid Stripe invoice, typically for recurring subscriptions."""
        subscription_id = invoice.get('subscription')
        if not subscription_id:
            _logger.info("Stripe invoice.paid event without a subscription ID.")
            return
        
        # Find the Odoo subscription linked to this Stripe subscription
        subscription = request.env['sale.subscription'].search([('acquirer_id.provider', '=', 'stripe'), ('acquirer_ref', '=', subscription_id)], limit=1)
        if not subscription:
            _logger.error("Could not find Odoo subscription for Stripe subscription ID %s", subscription_id)
            return
            
        user = subscription.partner_id.user_ids[:1]
        if not user:
            _logger.error("No user found for partner %s on subscription %s", subscription.partner_id.name, subscription.name)
            return
            
        # Logic to determine credits based on the subscription plan
        # This is where you would map subscription products to credit amounts or tiers
        line = subscription.recurring_invoice_line_ids and subscription.recurring_invoice_line_ids[0]
        if line and line.product_id.name == 'Pro Plan':
            user.sudo().write({'subscription_tier': 'Pro'})
            # Example: Pro plan gets 100 credits per month
            try:
                user.add_credits(100, f"Monthly credits for Pro Plan subscription {subscription.name}")
                _logger.info("Added 100 credits to user %s for Pro Plan renewal.", user.name)
            except UserError as e:
                _logger.error("Failed to add renewal credits to user %s: %s", user.name, e)

    @http.route('/payment/paypal/webhook', type='json', auth='public', csrf=False)
    def paypal_webhook(self, **post):
        """
        Placeholder for PayPal webhook.
        Logic would be similar to Stripe: verify the event, parse it,
        find the related Odoo record, and trigger business logic.
        """
        _logger.info("PayPal webhook received. Raw data: %s", pprint.pformat(request.jsonrequest))
        # 1. Verify the webhook event with PayPal's API.
        # 2. Parse the event type (e.g., 'PAYMENT.SALE.COMPLETED').
        # 3. Use custom_id or invoice_id to find the Odoo transaction.
        # 4. Trigger user.add_credits() or subscription confirmation.
        return http.Response(status=200)