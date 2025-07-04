from odoo import fields, models

class CreativeFlowGenerationRequest(models.Model):
    _name = 'creativeflow.generation_request'
    _description = 'CreativeFlow AI Generation Request'
    _order = 'create_date desc'

    name = fields.Char(string="Name", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        related='project_id.user_id',
        store=True,
        readonly=True
    )
    project_id = fields.Many2one(
        comodel_name='creativeflow.project',
        string="Project",
        required=True,
        ondelete='cascade'
    )
    prompt = fields.Text(string="Prompt", required=True)
    status = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        default='pending',
        required=True,
        index=True
    )
    error_message = fields.Text(string="Error Message", readonly=True)
    
    # Placeholder for the relation to generated assets
    # result_asset_ids = fields.One2many('creativeflow.asset', 'generation_request_id', string="Resulting Assets")

    credit_transaction_ids = fields.One2many(
        'creativeflow.credit_transaction', 
        'generation_request_id', 
        string="Credit Transactions"
    )

    def name_get(self):
        result = []
        for rec in self:
            name = f"[{rec.project_id.name}] - {rec.create_date.strftime('%Y-%m-%d')}"
            result.append((rec.id, name))
        return result