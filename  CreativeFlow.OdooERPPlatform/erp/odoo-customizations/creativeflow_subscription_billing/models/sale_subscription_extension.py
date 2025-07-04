# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleSubscriptionExtension(models.Model):
    """
    Extends 'sale.subscription' to add CreativeFlow specific logic,
    such as credit allotments on renewal and synchronization with the platform.
    """
    _inherit = 'sale.subscription'

    cf_platform_plan_id = fields.Char(
        string="CF Platform Plan ID",
        help="Identifier of the corresponding plan on the CreativeFlow platform."
    )
    cf_credit_allotment_per_cycle = fields.Float(
        string="CF Credits Allotment/Cycle",
        help="Credits to add to user's Odoo balance on successful renewal."
    )
    cf_last_sync_status_to_platform = fields.Datetime(
        string="Last Synced to Platform",
        readonly=True,
        copy=False
    )

    def _recurring_invoice(self, automatic=False):
        """
        Overrides the standard recurring invoice creation to add custom logic:
        1. Add credits to the partner if the plan includes a credit allotment.
           This happens AFTER the invoice is confirmed as paid.
        2. Trigger a synchronization action with the main platform.
        """
        invoices = super()._recurring_invoice(automatic=automatic)
        if not invoices:
            return invoices

        for sub in self.filtered(lambda s: s.cf_credit_allotment_per_cycle > 0):
            # The logic to add credits is now handled on payment confirmation
            # via the `_reconcile_and_create_credits` method on account.move,
            # which is called when an invoice linked to a subscription is paid.
            # This ensures credits are not given before payment is received.
            _logger.info("Subscription %s renewal invoice %s created. Credit allotment will be processed upon payment.", sub.name, invoices.filtered(lambda inv: inv.subscription_id == sub).name)

        self.action_sync_status_to_platform()
        return invoices

    def _reconcile_and_create_credits(self):
        """
        This method is designed to be called when a subscription invoice is paid.
        It handles the credit allotment.
        """
        super()._reconcile_and_create_credits()
        for sub in self:
            if sub.cf_credit_allotment_per_cycle > 0:
                description = _("Monthly credit allotment for subscription %s", sub.code)
                try:
                    sub.partner_id.add_credits(sub.cf_credit_allotment_per_cycle, description=description)
                    _logger.info("Added %s credits to partner %s for subscription %s.",
                                 sub.cf_credit_allotment_per_cycle, sub.partner_id.name, sub.code)
                    # Optionally create a note on the subscription or invoice
                    sub.message_post(body=_("Successfully added %s credits for this billing cycle.") % sub.cf_credit_allotment_per_cycle)
                except UserError as e:
                    _logger.error("Failed to add credits for partner %s (sub: %s): %s",
                                  sub.partner_id.name, sub.code, e)
                    sub.message_post(body=_("Error adding credits: %s") % e)


    def action_sync_status_to_platform(self):
        """
        Placeholder method for pushing subscription status changes to the main
        CreativeFlow platform. This would typically call an adapter service.
        """
        for sub in self:
            _logger.info("Syncing status for subscription %s to platform.", sub.name)
            # In a real implementation:
            # platform_adapter.update_subscription(sub.cf_platform_plan_id, {'status': sub.stage_id.category})
            sub.cf_last_sync_status_to_platform = fields.Datetime.now()
        return True

    def _handle_payment_failure(self, invoice):
        """
        Placeholder for handling dunning and payment failure logic.
        This could be triggered by a webhook when a payment fails.
        """
        self.ensure_one()
        _logger.warning("Payment failed for invoice %s linked to subscription %s. Initiating dunning process.",
                        invoice.name, self.name)
        # 1. Send dunning email
        # 2. Schedule retry
        # 3. Change subscription state if retries exhausted
        self.message_post(body=_("A payment has failed for invoice %s. Dunning process initiated.", invoice.name))
        return True