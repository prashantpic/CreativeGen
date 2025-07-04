# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ResUsersCreditMixin(models.Model):
    """
    Extends res.users with methods for managing credit balances and transactions.
    This includes debiting, crediting, and looking up action costs.
    """
    _inherit = 'res.users'

    credit_transaction_ids = fields.One2many(
        'creativeflow.credit.transaction', 'user_id',
        string="Credit Transactions",
        readonly=True
    )

    def _get_action_cost(self, action_identifier):
        """
        Retrieves the cost for a given action identifier.
        :param action_identifier: The unique string identifier for the action.
        :return: The cost of the action as a float.
        :raises: UserError if the action is not found or is inactive.
        """
        self.ensure_one()
        action_cost = self.env['creativeflow.credit.action.cost'].search([
            ('name', '=', action_identifier),
            ('is_active', '=', True)
        ], limit=1)
        if not action_cost:
            raise UserError(_("Action cost not defined or inactive for: %s") % action_identifier)
        return action_cost.cost

    def action_debit_credits(self, amount_to_debit, action_type, description, external_reference_model=None, external_reference_id=None, force_debit=False):
        """
        Debits a specified amount of credits from user balances and creates a transaction record.
        This method is designed to operate on a recordset of users.
        """
        transaction_env = self.env['creativeflow.credit.transaction']
        transactions = self.env['creativeflow.credit.transaction']

        for user in self:
            if not force_debit and user.credit_balance < amount_to_debit:
                raise UserError(_("Insufficient credits for %s. Required: %.4f, Available: %.4f") % (user.name, amount_to_debit, user.credit_balance))

            user.credit_balance -= amount_to_debit

            vals = {
                'user_id': user.id,
                'amount': -amount_to_debit,
                'type': action_type,
                'description': description,
                'balance_after_transaction': user.credit_balance,
                'external_reference_id': str(external_reference_id) if external_reference_id else False,
            }
            if external_reference_model and external_reference_id:
                vals['reference_document'] = f"{external_reference_model},{external_reference_id}"

            new_transaction = transaction_env.create(vals)
            transactions |= new_transaction

        return transactions

    def action_credit_credits(self, amount_to_credit, action_type, description, external_reference_model=None, external_reference_id=None):
        """
        Credits a specified amount to user balances and creates a transaction record.
        This method is designed to operate on a recordset of users.
        """
        transaction_env = self.env['creativeflow.credit.transaction']
        transactions = self.env['creativeflow.credit.transaction']

        if amount_to_credit <= 0:
            raise UserError(_("Amount to credit must be positive."))

        for user in self:
            user.credit_balance += amount_to_credit

            vals = {
                'user_id': user.id,
                'amount': amount_to_credit,
                'type': action_type,
                'description': description,
                'balance_after_transaction': user.credit_balance,
                'external_reference_id': str(external_reference_id) if external_reference_id else False,
            }
            if external_reference_model and external_reference_id:
                vals['reference_document'] = f"{external_reference_model},{external_reference_id}"

            new_transaction = transaction_env.create(vals)
            transactions |= new_transaction

        return transactions


    def api_debit_credits_by_action_identifier(self, action_identifier, description_prefix="", external_reference_model=None, external_reference_id=None, force_debit=False):
        """
        High-level API to debit credits based on a pre-configured action identifier.
        This method operates on a single user record.
        """
        self.ensure_one()
        cost = self._get_action_cost(action_identifier)
        action_config = self.env['creativeflow.credit.action.cost'].search([('name', '=', action_identifier)], limit=1)

        description = _("%s%s (Cost: %.4f credits)") % (
            f"{description_prefix}: " if description_prefix else "",
            action_config.description or action_identifier,
            cost
        )

        # Basic mapping from action identifier to transaction type.
        # This could be more sophisticated if needed.
        mapped_action_type = action_identifier
        if mapped_action_type not in [key for key, val in self.env['creativeflow.credit.transaction']._fields['type'].selection]:
            mapped_action_type = 'other_debit'

        return self.action_debit_credits(cost, mapped_action_type, description, external_reference_model, external_reference_id, force_debit=force_debit)