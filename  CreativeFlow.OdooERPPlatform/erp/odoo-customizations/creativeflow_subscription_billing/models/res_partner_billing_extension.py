# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartnerBillingExtension(models.Model):
    """
    Extends 'res.partner' to manage CreativeFlow's Odoo-side billing
    information, such as credit balance and related subscriptions.
    """
    _inherit = 'res.partner'

    cf_credit_balance = fields.Float(
        string="CF Credit Balance (Odoo Managed)",
        digits=(16, 4),
        default=0.0,
        copy=False,
        help="User's credit balance managed within Odoo for platform features."
    )
    cf_subscription_ids = fields.One2many(
        comodel_name='sale.subscription',
        inverse_name='partner_id',
        string="CF Subscriptions",
        readonly=True,
    )
    cf_credit_log_ids = fields.One2many(
        comodel_name='creativeflow.credit.log',
        inverse_name='partner_id',
        string="CF Credit Logs",
        readonly=True,
    )

    def _create_credit_transaction_log(self, amount, description, transaction_type,
                                       related_document_model=None, related_document_id=None):
        """
        Private helper to create a credit log entry.
        :return: created creativeflow.credit.log record
        """
        self.ensure_one()
        log_vals = {
            'partner_id': self.id,
            'amount': amount,
            'description': description,
            'transaction_type': transaction_type,
            'related_document_model': related_document_model,
            'related_document_id': related_document_id,
        }
        return self.env['creativeflow.credit.log'].create(log_vals)

    def add_credits(self, amount, description=None, force_commit=False):
        """
        Adds a specified amount of credits to the partner's balance.

        :param float amount: The positive amount of credits to add.
        :param str description: Optional description for the transaction log.
        :param bool force_commit: If True, commit the transaction immediately.
        :return: The created creativeflow.credit.log record.
        """
        self.ensure_one()
        if amount <= 0:
            raise UserError(_("Credit amount must be positive."))

        self.cf_credit_balance += amount
        log_record = self._create_credit_transaction_log(amount, description, 'addition')

        if force_commit:
            self.env.cr.commit()

        return log_record

    def deduct_credits(self, amount, description=None, related_document_model=None,
                       related_document_id=None, force_commit=False):
        """
        Deducts a specified amount of credits from the partner's balance.

        :param float amount: The positive amount of credits to deduct.
        :param str description: Optional description for the transaction log.
        :param str related_document_model: Optional model name of related document.
        :param int related_document_id: Optional ID of related document.
        :param bool force_commit: If True, commit the transaction immediately.
        :return: The created creativeflow.credit.log record.
        :raises UserError: If amount is not positive or if credits are insufficient.
        """
        self.ensure_one()
        if amount <= 0:
            raise UserError(_("Credit amount to deduct must be positive."))

        if self.cf_credit_balance < amount:
            raise UserError(_("Insufficient credits. Partner '%s' has %s but %s are required.") %
                            (self.name, self.cf_credit_balance, amount))

        self.cf_credit_balance -= amount
        log_record = self._create_credit_transaction_log(
            -amount, description, 'deduction', related_document_model, related_document_id
        )

        if force_commit:
            self.env.cr.commit()

        return log_record