from odoo import fields, models

class HelpdeskTicketExtension(models.Model):
    _inherit = 'helpdesk.ticket'

    project_id = fields.Many2one(
        comodel_name='creativeflow.project',
        string="Related Project",
        help="Link this ticket to a specific creative project."
    )
    generation_request_id = fields.Many2one(
        comodel_name='creativeflow.generation_request',
        string="Related Generation Request",
        help="Link this ticket to a specific AI generation request."
    )