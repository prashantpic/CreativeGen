# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class BillingService(models.AbstractModel):
    """
    Abstract model acting as a service layer for complex billing operations.
    This service is called by webhook controllers and other parts of the system
    to orchestrate billing logic.
    """
    _name = 'billing.service'
    _description = 'CreativeFlow Billing Service'

    def process_stripe_payment_event(self, event_object, acquirer_id):
        """
        Process a verified Stripe event.

        :param dict event_object: The Stripe event object.
        :param int acquirer_id: The ID of the payment.acquirer record.
        """
        event_type = event_object.get('type')
        _logger.info("Processing Stripe event '%s'", event_type)

        # Idempotency check: ensure we don't process the same event twice
        if self.env['payment.transaction'].sudo().search_count([('acquirer_reference', '=', event_object.get('id'))]):
            _logger.info("Event %s already processed. Skipping.", event_object.get('id'))
            return

        if event_type == 'invoice.payment_succeeded':
            self._handle_stripe_invoice_payment_succeeded(event_object, acquirer_id)
        elif event_type == 'invoice.payment_failed':
            self._handle_stripe_invoice_payment_failed(event_object, acquirer_id)
        elif event_type in ('customer.subscription.updated', 'customer.subscription.deleted'):
            self._handle_stripe_subscription_change(event_object, acquirer_id)
        elif event_type == 'charge.refunded':
            self._handle_stripe_charge_refunded(event_object, acquirer_id)
        else:
            _logger.info("Unhandled Stripe event type: %s", event_type)

    def _handle_stripe_invoice_payment_succeeded(self, event, acquirer_id):
        """Handle successful payment for a Stripe invoice."""
        invoice_data = event['data']['object']
        subscription_stripe_id = invoice_data.get('subscription')
        if not subscription_stripe_id:
            _logger.info("Stripe invoice.payment_succeeded event for non-subscription invoice. Skipping credit logic.")
            return

        subscription = self.env['sale.subscription'].sudo().search(
            [('acquirer_id', '=', acquirer_id), ('acquirer_reference', '=', subscription_stripe_id)], limit=1)

        if not subscription:
            _logger.warning("Received payment success for unknown Stripe subscription ID: %s", subscription_stripe_id)
            return

        # Find the related Odoo invoice and mark it as paid if not already
        tx = self.env['payment.transaction'].sudo().search([('acquirer_reference', '=', invoice_data.get('payment_intent'))])
        if tx and tx.invoice_ids:
            for invoice in tx.invoice_ids:
                if invoice.payment_state != 'paid':
                    # This should trigger the credit allotment via the overridden _reconcile_and_create_credits
                     _logger.info("Payment transaction %s for invoice %s confirmed by webhook.", tx.reference, invoice.name)

        _logger.info("Successfully processed payment for subscription %s.", subscription.code)
        subscription.message_post(body=_("Subscription payment confirmed via Stripe webhook for invoice %s.", invoice_data.get('number')))


    def _handle_stripe_invoice_payment_failed(self, event, acquirer_id):
        """Handle failed payment for a Stripe invoice."""
        invoice_data = event['data']['object']
        subscription_stripe_id = invoice_data.get('subscription')
        if not subscription_stripe_id:
            return

        subscription = self.env['sale.subscription'].sudo().search(
            [('acquirer_reference', '=', subscription_stripe_id)], limit=1)

        if subscription:
            # Find the Odoo invoice to pass to the failure handler
            odoo_invoice = self.env['account.move'].sudo().search([('ref', '=', invoice_data.get('number'))], limit=1)
            subscription._handle_payment_failure(odoo_invoice)

    def _handle_stripe_subscription_change(self, event, acquirer_id):
        """Handle subscription updates or cancellations from Stripe."""
        subscription_data = event['data']['object']
        subscription_stripe_id = subscription_data.get('id')
        subscription = self.env['sale.subscription'].sudo().search(
            [('acquirer_id', '=', acquirer_id), ('acquirer_reference', '=', subscription_stripe_id)], limit=1)

        if not subscription:
            return

        new_status = subscription_data.get('status')
        if new_status == 'canceled' or subscription_data.get('cancel_at_period_end'):
            subscription.close_subscription()
            subscription.message_post(body=_("Subscription cancelled in Stripe."))
        # Add more status mappings if needed
        subscription.action_sync_status_to_platform()

    def _handle_stripe_charge_refunded(self, event, acquirer_id):
        """Handle a refunded charge from Stripe."""
        _logger.info("Processing charge.refunded event.")
        # Logic to find the original payment, create a credit note, and potentially deduct credits.

    def process_paypal_payment_event(self, event_data, acquirer_id):
        """
        Process a verified PayPal event. Placeholder for actual logic.
        """
        _logger.info("Processing PayPal event: %s", event_data.get('event_type'))
        # Similar logic to Stripe: dispatch based on event type, find records, update state.

    def apply_taxes_to_invoice_line(self, invoice_line):
        """
        Ensures correct taxes are applied. Odoo's standard fiscal position logic
        usually handles this. This is a hook for custom overrides.
        """
        _logger.info("Applying custom tax logic for invoice line %s (Placeholder).", invoice_line.id)
        # Odoo's standard tax computation is typically sufficient.

    def initiate_dunning_for_subscription(self, subscription_id):
        """
        Manages the dunning process for a subscription with a failed payment.
        """
        subscription = self.env['sale.subscription'].browse(subscription_id)
        _logger.info("Initiating dunning process for subscription %s (Placeholder).", subscription.code)
        # Logic for sending dunning emails, scheduling retries, and updating status.