import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CreativeFlowUser(models.Model):
    """
    Extends the built-in res.users model with platform-specific fields and logic
    for managing user subscription, credits, and related creative assets.
    """
    _inherit = 'res.users'

    subscription_tier = fields.Selection(
        selection=[
            ('Free', 'Free'),
            ('Pro', 'Pro'),
            ('Team', 'Team'),
            ('Enterprise', 'Enterprise')
        ],
        string="Subscription Tier",
        default='Free',
        required=True,
        help="The user's current subscription plan."
    )
    credit_balance = fields.Float(
        string="Credit Balance",
        default=0.0,
        digits=(10, 2),
        readonly=True,
        help="Cached credit balance. The source of truth is the sum of all credit transactions."
    )
    x_studio_brand_kit_ids = fields.One2many(
        comodel_name='creativeflow.brand_kit',
        inverse_name='user_id',
        string="Brand Kits"
    )
    x_studio_workbench_ids = fields.One2many(
        comodel_name='creativeflow.workbench',
        inverse_name='user_id',
        string="Workbenches"
    )

    def deduct_credits(self, amount: float, description: str, generation_request_id: int = None) -> bool:
        """
        Deducts a specified amount of credits from the user's balance.
        This operation is atomic per user. It creates a transaction record for auditing.

        :param amount: The amount of credits to deduct. Must be positive.
        :param description: A clear description of why credits are being deducted.
        :param generation_request_id: Optional ID of the related generation request.
        :return: True if the deduction was successful.
        :raises: odoo.exceptions.UserError if the user has insufficient credits.
        """
        if amount <= 0:
            raise UserError(_("Credit deduction amount must be positive."))

        for user in self:
            if user.credit_balance < amount:
                _logger.warning(
                    "Failed credit deduction for user %s (ID: %s). "
                    "Requested: %.2f, Available: %.2f",
                    user.name, user.id, amount, user.credit_balance
                )
                raise UserError(_(
                    "Insufficient credits. You need %.2f credits for this action, but you only have %.2f.",
                    amount, user.credit_balance
                ))

            vals = {
                'user_id': user.id,
                'amount': -amount,
                'description': description,
            }
            if generation_request_id:
                vals['generation_request_id'] = generation_request_id

            self.env['creativeflow.credit_transaction'].sudo().create(vals)
            # Use sudo() for creation as this might be called from controllers
            # where the current user doesn't have write access on the transaction model.

            new_balance = user.credit_balance - amount
            user.sudo().write({'credit_balance': new_balance})
            _logger.info(
                "Deducted %.2f credits from user %s (ID: %s). New balance: %.2f. Reason: %s",
                amount, user.name, user.id, new_balance, description
            )
        return True

    def add_credits(self, amount: float, description: str, related_invoice_id: int = None) -> bool:
        """
        Adds a specified amount of credits to the user's balance.
        Creates a transaction record for auditing.

        :param amount: The amount of credits to add. Must be positive.
        :param description: A clear description of why credits are being added.
        :param related_invoice_id: Optional ID of the invoice related to this credit purchase.
        :return: True on success.
        """
        if amount <= 0:
            raise UserError(_("Credit addition amount must be positive."))

        for user in self:
            vals = {
                'user_id': user.id,
                'amount': amount,
                'description': description,
            }
            if related_invoice_id:
                vals['related_invoice_id'] = related_invoice_id

            self.env['creativeflow.credit_transaction'].sudo().create(vals)

            new_balance = user.credit_balance + amount
            user.sudo().write({'credit_balance': new_balance})
            _logger.info(
                "Added %.2f credits to user %s (ID: %s). New balance: %.2f. Reason: %s",
                amount, user.name, user.id, new_balance, description
            )
        return True