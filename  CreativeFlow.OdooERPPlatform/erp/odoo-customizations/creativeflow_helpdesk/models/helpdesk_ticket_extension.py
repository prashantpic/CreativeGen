# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HelpdeskTicketExtension(models.Model):
    """
    Extends 'helpdesk.ticket' to add fields providing more context
    about the user and the issue, specific to the CreativeFlow platform.
    """
    _inherit = 'helpdesk.ticket'

    cf_related_feature_area = fields.Selection(
        selection=[
            ('general', 'General Inquiry'),
            ('ai_generation', 'AI Generation'),
            ('billing', 'Billing & Subscription'),
            ('account', 'Account Management'),
            ('mobile_app', 'Mobile App'),
            ('api', 'API Usage'),
            ('bug_report', 'Bug Report'),
            ('feature_request', 'Feature Request')
        ],
        string="CF Feature Area",
        help="The area of the CreativeFlow platform this ticket relates to."
    )
    cf_user_subscription_tier_at_creation = fields.Char(
        string="User Subscription Tier (at ticket creation)",
        compute='_compute_cf_user_subscription_tier',
        store=True,
        readonly=True,
        help="The user's subscription tier, captured when the ticket is created."
    )

    @api.depends('partner_id')
    def _compute_cf_user_subscription_tier(self):
        """
        Computes the user's subscription tier based on the synced data
        on the partner record. This is triggered when the partner is set.
        """
        for ticket in self:
            if ticket.partner_id and ticket.partner_id.cf_synced_subscription_tier:
                ticket.cf_user_subscription_tier_at_creation = ticket.partner_id.cf_synced_subscription_tier
            else:
                ticket.cf_user_subscription_tier_at_creation = 'Unknown'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to ensure the compute method is triggered if partner_id is present.
        The `store=True` on the compute field already handles this, but this
        is an explicit way to ensure it's set on creation.
        """
        tickets = super().create(vals_list)
        tickets._compute_cf_user_subscription_tier()
        return tickets