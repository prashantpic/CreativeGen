from odoo import api, fields, models

class CreativeFlowProject(models.Model):
    _name = 'creativeflow.project'
    _description = 'CreativeFlow Project'
    _order = 'name'

    name = fields.Char(string="Project Name", required=True)
    workbench_id = fields.Many2one(
        comodel_name='creativeflow.workbench',
        string="Workbench",
        required=True,
        ondelete='cascade'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        related='workbench_id.user_id',
        store=True,
        readonly=True
    )
    brand_kit_id = fields.Many2one(
        comodel_name='creativeflow.brand_kit',
        string="Brand Kit",
        help="Override the workbench's default brand kit for this specific project.",
        domain="[('user_id', '=', user_id)]"
    )
    asset_ids = fields.One2many(
        # The 'creativeflow.asset' model will be defined in a separate module.
        # Odoo will resolve this relationship once that module is installed.
        comodel_name='creativeflow.asset',
        inverse_name='project_id',
        string="Assets"
    )
    generation_request_ids = fields.One2many(
        comodel_name='creativeflow.generation_request',
        inverse_name='project_id',
        string="Generation Requests"
    )

    @api.onchange('workbench_id')
    def _onchange_workbench_id(self):
        """ Automatically populates the brand kit from the workbench's default. """
        if self.workbench_id and self.workbench_id.default_brand_kit_id:
            self.brand_kit_id = self.workbench_id.default_brand_kit_id
        else:
            self.brand_kit_id = False