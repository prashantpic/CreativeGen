# -*- coding: utf-8 -*-
import json
import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    import stripe
except ImportError:
    _logger.warning("Stripe library not installed, please install it with `pip install stripe`")
    stripe = None


class PaymentWebhookController(http.Controller):

    @http.route('/payment/stripe/webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def stripe_webhook(self, **kwargs):
        """
        Webhook endpoint for receiving and processing events from Stripe.
        Verifies the webhook signature and dispatches the event to the billing service.
        """
        if not stripe:
            _logger.error("Stripe library is not available.")
            return http.Response("Stripe library not installed on server.", status=500)

        payload = request.httprequest.data
        sig_header = request.httprequest.headers.get('Stripe-Signature')

        # The acquirer could be identified from the payload, or a specific endpoint per acquirer could be used.
        # For simplicity, we assume one primary Stripe acquirer for now.
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'stripe')], limit=1)
        if not acquirer:
            _logger.error("No Stripe payment acquirer found in the system.")
            return http.Response("Payment acquirer not configured.", status=500)

        webhook_secret = acquirer.cf_webhook_secret
        if not webhook_secret:
            _logger.error("Webhook secret is not configured for Stripe acquirer '%s'", acquirer.name)
            return http.Response("Webhook secret not configured.", status=500)

        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=webhook_secret
            )
        except ValueError as e:
            # Invalid payload
            _logger.warning("Stripe webhook processing failed: Invalid payload. %s", e)
            return http.Response("Invalid payload", status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            _logger.warning("Stripe webhook processing failed: Invalid signature. %s", e)
            return http.Response("Invalid signature", status=400)
        except Exception as e:
            _logger.error("An unexpected error occurred during Stripe webhook event construction: %s", e)
            return http.Response("Internal server error", status=500)

        _logger.info("Stripe webhook event received: %s", pprint.pformat(event))
        try:
            # Using a specific service for processing is cleaner
            request.env['billing.service'].sudo().process_stripe_payment_event(event, acquirer.id)
        except Exception as e:
            _logger.exception("Error processing Stripe event type %s: %s", event.get('type'), e)
            return http.Response("Error processing event", status=500)

        return http.Response(status=200)

    @http.route('/payment/paypal/webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def paypal_webhook(self, **kwargs):
        """
        Webhook endpoint for receiving and processing events from PayPal.
        This is a placeholder and requires implementation of PayPal's webhook
        verification logic.
        """
        _logger.info("PayPal webhook received: %s", pprint.pformat(request.jsonrequest))
        payload = request.jsonrequest
        if not payload:
            return http.Response("Invalid payload", status=400)

        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'paypal')], limit=1)
        if not acquirer:
            _logger.error("No PayPal payment acquirer found in the system.")
            return http.Response("Payment acquirer not configured.", status=500)

        # PayPal webhook verification is more complex, often requiring an API call back to PayPal.
        # This is a conceptual placeholder for that logic.
        # verified = acquirer._paypal_verify_webhook_signature(request.httprequest.headers, request.httprequest.data)
        # if not verified:
        #     _logger.warning("PayPal webhook signature verification failed.")
        #     return http.Response("Invalid signature", status=400)

        try:
            request.env['billing.service'].sudo().process_paypal_payment_event(payload, acquirer.id)
        except Exception as e:
            _logger.exception("Error processing PayPal event: %s", e)
            return http.Response("Error processing event", status=500)

        return http.Response(status=200)