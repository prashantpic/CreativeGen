# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductTemplate(models.Model):
    """
    Extends the product.template model to add fields for defining how a
    product relates to a CreativeFlow subscription tier and credit grants.
    """
    _inherit = 'product.template'

    cf_subscription_tier_provided = fields.Selection(
        selection=[
            ('free', 'Free'),
            ('pro', 'Pro'),
            ('team', 'Team'),
            ('enterprise', 'Enterprise')
        ],
        string="CreativeFlow Tier Provided",
        help="The CreativeFlow subscription tier this product represents when sold as a subscription."
    )

    cf_credits_granted_on_period_start = fields.Float(
        string="Credits Granted Per Period",
        digits=(16, 4),
        default=0.0,
        help="Number of credits automatically granted to the user when a subscription period for this product starts/renews."
    )