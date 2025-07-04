# -*- coding: utf-8 -*-

from odoo import fields, models

class CreditActionCost(models.Model):
    """
    Configuration model to define the cost in credits for various billable
    actions performed on the CreativeFlow platform.
    """
    _name = 'creativeflow.credit.action.cost'
    _description = 'CreativeFlow Credit Action Cost'

    name = fields.Char(
        string="Action Name / Identifier",
        required=True,
        index=True,
        help="Unique identifier for the billable action, e.g., 'sample_generation', 'final_generation_standard_res', 'export_hd', 'api_call_model_x'."
    )
    cost = fields.Float(
        string="Credit Cost",
        required=True,
        digits=(16, 4),
        help="Number of credits this action costs. Can be 0 for free actions under certain plans."
    )
    description = fields.Text(
        string="Description"
    )
    is_active = fields.Boolean(
        string="Active",
        default=True,
        help="Only active costs are considered for billing."
    )

    _sql_constraints = [
        ('unique_action_name', 'UNIQUE(name)', "An action with this identifier already exists!")
    ]