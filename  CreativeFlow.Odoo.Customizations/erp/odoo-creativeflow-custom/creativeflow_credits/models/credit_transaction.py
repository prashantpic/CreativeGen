# -*- coding: utf-8 -*-

from odoo import fields, models

class CreditTransaction(models.Model):
    """
    Represents a single credit transaction for a user, serving as an immutable
    log of all credit additions and deductions.
    """
    _name = 'creativeflow.credit.transaction'
    _description = 'CreativeFlow Credit Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'transaction_date desc, id desc'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        required=True,
        ondelete='cascade',
        index=True
    )
    amount = fields.Float(
        string="Amount",
        required=True,
        digits=(16, 4),
        help="Positive for credit (addition to balance), negative for debit (deduction from balance)."
    )
    balance_after_transaction = fields.Float(
        string="Balance After",
        digits=(16, 4),
        readonly=True,
        help="User's credit balance after this transaction was applied."
    )
    type = fields.Selection(
        selection=[
            ('purchase', 'Purchase'),
            ('refund', 'Refund'),
            ('adjustment_add', 'Adjustment (Add)'),
            ('adjustment_deduct', 'Adjustment (Deduct)'),
            ('sample_generation', 'Sample Generation'),
            ('final_generation', 'Final Generation'),
            ('export_hd', 'HD Export'),
            ('api_usage', 'API Usage'),
            ('other_debit', 'Other Debit'),
            ('other_credit', 'Other Credit')
        ],
        string="Type",
        required=True,
        help="Categorizes the credit transaction."
    )
    description = fields.Text(
        string="Description",
        help="Details about the transaction, e.g., 'Purchase of 100 credits', 'Cost for generating image X'."
    )
    reference_document = fields.Reference(
        selection=[
            ('creativeflow.generation.request.external', 'Generation Request (External)'),
            ('creativeflow.api.call.external', 'API Call (External)'),
            ('sale.order', 'Sale Order/Invoice')
        ],
        string="Reference Document",
        help="Link to the originating document if applicable (e.g., an Odoo Sale Order for credit purchase, or an external generation request ID)."
    )
    external_reference_id = fields.Char(
        string="External Reference ID",
        help="Stores the ID of the external document (e.g., Generation Request ID, API Call ID)."
    )
    transaction_date = fields.Datetime(
        string="Date",
        default=fields.Datetime.now,
        required=True,
        readonly=True
    )