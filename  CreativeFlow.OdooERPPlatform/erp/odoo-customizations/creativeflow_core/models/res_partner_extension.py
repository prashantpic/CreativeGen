# -*- coding: utf-8 -*-
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartnerExtension(models.Model):
    """
    Extends the 'res.partner' model to include fields relevant to
    CreativeFlow's administrative views within Odoo. These fields are
    typically read-only and are populated by synchronization mechanisms
    from the main platform.
    """
    _inherit = 'res.partner'

    cf_synced_credit_balance = fields.Float(
        string="CF Credit Balance (Synced)",
        readonly=True,
        help="User's credit balance synced from the platform.",
        groups="base.group_user"
    )
    cf_synced_subscription_tier = fields.Char(
        string="CF Subscription Tier (Synced)",
        readonly=True,
        help="User's subscription tier synced from the platform.",
        groups="base.group_user"
    )

    def action_sync_with_platform(self):
        """
        Placeholder method to trigger a synchronization with the main
        CreativeFlow platform.

        The actual synchronization logic is expected to be handled by an
        external service or a scheduled cron job that calls an API endpoint.
        This method can be used for manual triggers for debugging or
        administrative purposes.
        """
        _logger.info("Placeholder action 'action_sync_with_platform' triggered for partners: %s", self.ids)
        # In a real implementation, this might call an adapter service:
        # for partner in self:
        #     try:
        #         # platform_adapter.sync_partner_data(partner.id)
        #         pass
        #     except Exception as e:
        #         _logger.error("Failed to sync partner %s: %s", partner.id, e)
        pass