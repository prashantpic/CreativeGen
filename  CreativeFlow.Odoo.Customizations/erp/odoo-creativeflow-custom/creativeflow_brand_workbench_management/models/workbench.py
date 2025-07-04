# -*- coding: utf-8 -*-

from odoo import fields, models

class Workbench(models.Model):
    """
    Represents a CreativeFlow Workbench, which acts as a container or
    workspace for organizing creative projects.
    """
    _name = 'creativeflow.workbench'
    _description = 'CreativeFlow Workbench'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Owner",
        required=True,
        index=True,
        default=lambda self: self.env.user
    )
    default_brand_kit_id = fields.Many2one(
        comodel_name='creativeflow.brand.kit',
        string="Default Brand Kit",
        domain="[('user_id', '=', user_id)]",
        help="The default brand kit to be suggested for new projects within this workbench."
    )
    cf_project_ids_external = fields.Text(
        string="CreativeFlow Project IDs (JSON)",
        help="JSON list of external CreativeFlow project identifiers belonging to this workbench."
    )
    cf_external_workbench_id = fields.Char(
        string="CreativeFlow Workbench ID (External)",
        index=True,
        copy=False
    )