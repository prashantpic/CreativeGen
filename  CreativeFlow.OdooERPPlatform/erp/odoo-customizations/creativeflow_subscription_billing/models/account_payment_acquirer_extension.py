# -*- coding: utf-8 -*-

from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class PaymentAcquirerExtension(models.Model):
    """
    Extends 'payment.acquirer' to store CreativeFlow specific configurations,
    such as webhook secrets for signature verification.
    """
    _inherit = 'payment.acquirer'

    cf_custom_config = fields.Text(
        string="CF Custom Configuration",
        help="JSON or text field for specific acquirer configurations needed by CreativeFlow."
    )
    cf_webhook_secret = fields.Char(
        string="CF Webhook Secret",
        help="Secret key for verifying webhook signatures, stored securely.",
        copy=False,
        groups='base.group_system'  # Restrict access to administrators
    )

    def _stripe_verify_webhook_signature(self, signature_header, payload_body):
        """
        Placeholder for Stripe webhook signature verification.
        The actual implementation is in the controller to have access to the request.
        """
        self.ensure_one()
        _logger.info("Calling Stripe webhook signature verification for acquirer %s", self.name)
        if not self.cf_webhook_secret:
            _logger.error("Webhook secret is not configured for Stripe acquirer %s.", self.name)
            return False
        # The logic using stripe.Webhook.construct_event will be in the controller.
        return True

    def _paypal_verify_webhook_signature(self, headers, payload_body):
        """
        Placeholder for PayPal webhook signature verification.
        """
        self.ensure_one()
        _logger.info("Calling PayPal webhook signature verification for acquirer %s", self.name)
        # Actual PayPal verification logic would go here.
        return True