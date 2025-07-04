import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    def _recurring_create_invoice(self, automatic=False, batch_size=30):
        """
        Overrides the standard invoice creation to add custom logic after
        a recurring invoice is generated. The actual credit addition is handled
        by payment confirmation webhooks for better accuracy. This method could
        be used for pre-emptive logic or logging.
        """
        _logger.info("CreativeFlow: _recurring_create_invoice initiated.")
        invoices = super(SaleSubscription, self)._recurring_create_invoice(automatic, batch_size)
        
        # Post-invoice creation logic can be added here.
        # For example, logging that a subscription is due for renewal.
        for invoice in invoices:
            _logger.info(
                "Invoice %s created for subscription %s for partner %s.",
                invoice.name, invoice.subscription_id.name, invoice.partner_id.name
            )

        return invoices

    def _reconcile_and_send_invoices(self, batch_size=30):
        """
        After invoices are reconciled (paid), custom logic could be triggered.
        However, the recommended approach is to rely on payment provider webhooks
        which are more instantaneous and reliable.
        """
        _logger.info("CreativeFlow: _reconcile_and_send_invoices initiated.")
        res = super(SaleSubscription, self)._reconcile_and_send_invoices(batch_size)
        # Any logic here would run after payment has been reconciled in Odoo.
        return res