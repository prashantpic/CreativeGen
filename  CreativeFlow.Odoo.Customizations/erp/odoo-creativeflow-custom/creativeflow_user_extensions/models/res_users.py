# -*- coding: utf-8 -*-

from odoo import fields, models

class ResUsers(models.Model):
    """
    Extends the standard res.users model to include fields specific to the
    CreativeFlow platform, facilitating integration and data synchronization.
    """
    _inherit = 'res.users'

    credit_balance = fields.Float(
        string="Credit Balance",
        digits=(16, 4),
        readonly=True,
        default=0.0,
        tracking=True,
        help="User's current credit balance, primarily managed by the CreativeFlow Credit System module but displayed here for information. This field is typically updated by automated processes or credit transactions."
    )

    cf_subscription_tier = fields.Selection(
        selection=[
            ('free', 'Free'),
            ('pro', 'Pro'),
            ('team', 'Team'),
            ('enterprise', 'Enterprise')
        ],
        string="CreativeFlow Subscription Tier",
        default='free',
        tracking=True,
        help="The user's current subscription tier on the CreativeFlow platform."
    )

    cf_external_user_id = fields.Char(
        string="CreativeFlow Platform User ID",
        index=True,
        help="Unique User ID from the main CreativeFlow platform, used for synchronization and API calls. This helps link the Odoo user to their primary platform account if Odoo is not the master identity provider."
    )

    cf_language_preference = fields.Char(
        string="CreativeFlow Language Preference",
        size=10,
        default='en-US',
        help="User's preferred language for the CreativeFlow platform UI (e.g., 'en-US', 'es-ES')."
    )

    cf_timezone = fields.Char(
        string="CreativeFlow Timezone",
        size=50,
        default='UTC',
        help="User's preferred timezone for localized date/time display."
    )