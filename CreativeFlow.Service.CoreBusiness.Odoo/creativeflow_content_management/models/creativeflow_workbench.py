from odoo import api, fields, models

class CreativeFlowWorkbench(models.Model):
    _name = 'creativeflow.workbench'
    _description = 'CreativeFlow Workbench'
    _order = 'name'

    name = fields.Char(string="Workbench Name", required=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        required=True,
        ondelete='cascade',
        default=lambda self: self.env.user
    )
    project_ids = fields.One2many(
        comodel_name='creativeflow.project',
        inverse_name='workbench_id',
        string="Projects"
    )
    default_brand_kit_id = fields.Many2one(
        comodel_name='creativeflow.brand_kit',
        string="Default Brand Kit",
        domain="[('user_id', '=', user_id)]",
        help="The default brand kit to be used for new projects in this workbench."
    )
    project_count = fields.Integer(string="Project Count", compute='_compute_project_count')

    @api.depends('project_ids')
    def _compute_project_count(self):
        for workbench in self:
            workbench.project_count = len(workbench.project_ids)