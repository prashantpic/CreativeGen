from odoo import fields, models

class CreativeFlowCreditTransaction(models.Model):
    _name = 'creativeflow.credit_transaction'
    _description = 'CreativeFlow Credit Transaction Log'
    _order = 'create_date desc'
    _log_access = False # High volume table, no need to log every read/write

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        required=True,
        ondelete='restrict'
    )
    amount = fields.Float(
        string="Amount",
        required=True,
        digits=(10, 2),
        help="The amount of credits transacted. Positive for additions, negative for deductions."
    )
    description = fields.Char(string="Description", required=True)
    generation_request_id = fields.Many2one(
        comodel_name='creativeflow.generation_request',
        string="Related Generation Request",
        ondelete='set null'
    )
    related_invoice_id = fields.Many2one(
        comodel_name='account.move',
        string="Related Invoice",
        ondelete='set null'
    )

    def init(self):
        # Prevent modification of records
        self.env.cr.execute("""
            CREATE OR REPLACE RULE credit_transaction_update_block AS
            ON UPDATE TO %s DO INSTEAD NOTHING;
        """ % self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE RULE credit_transaction_delete_block AS
            ON DELETE TO %s DO INSTEAD NOTHING;
        """ % self._table)