# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CreativeflowCreditLog(models.Model):
    """
    This model logs all credit transactions for CreativeFlow partners,
    providing a clear audit trail of credit additions and deductions.
    """
    _name = 'creativeflow.credit.log'
    _description = 'CreativeFlow Credit Transaction Log'
    _order = 'date_transaction desc, id desc'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
        required=True,
        ondelete='cascade',
        index=True,
    )
    amount = fields.Float(
        string="Amount",
        digits=(16, 4),
        required=True,
        help="The amount of credits transacted. Positive for additions, negative for deductions."
    )
    description = fields.Text(
        string="Description"
    )
    transaction_type = fields.Selection(
        selection=[
            ('addition', 'Addition'),
            ('deduction', 'Deduction'),
            ('initial', 'Initial Balance'),
            ('refund', 'Refund')
        ],
        string="Type",
        required=True
    )
    date_transaction = fields.Datetime(
        string="Transaction Date",
        required=True,
        default=fields.Datetime.now,
        index=True
    )
    related_document_model = fields.Char(
        string="Related Document Model",
        help="The model of the document that triggered this transaction (e.g., 'sale.order', 'account.move')."
    )
    related_document_id = fields.Integer(
        string="Related Document ID",
        help="The ID of the document that triggered this transaction."
    )
    related_document_display = fields.Char(
        string="Related Document",
        compute='_compute_related_document_display',
        store=False,
        help="Display name of the related document."
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='partner_id.company_id',
        store=True
    )

    @api.depends('related_document_model', 'related_document_id')
    def _compute_related_document_display(self):
        """
        Computes the display name of the related document for easier
        identification in the user interface.
        """
        for log in self:
            log.related_document_display = ""
            if log.related_document_model and log.related_document_id:
                try:
                    related_record = self.env[log.related_document_model].browse(log.related_document_id).exists()
                    if related_record:
                        log.related_document_display = related_record.display_name
                except (KeyError, AttributeError):
                    # Model does not exist or record was deleted
                    log.related_document_display = f"{log.related_document_model} #{log.related_document_id} (Not found)"