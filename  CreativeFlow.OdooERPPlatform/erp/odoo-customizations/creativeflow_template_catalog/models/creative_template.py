# -*- coding: utf-8 -*-
from odoo import fields, models


class CreativeTemplate(models.Model):
    """
    Model to store and manage metadata for CreativeFlow AI templates.
    Allows administrators to manage the template library from within Odoo.
    """
    _name = 'creativeflow.template'
    _description = 'CreativeFlow AI Template'
    _order = 'sequence, name'

    name = fields.Char(
        string="Template Name",
        required=True,
        translate=True
    )
    sequence = fields.Integer(string="Sequence", default=10)
    description = fields.Text(
        string="Description",
        translate=True
    )
    category_id = fields.Many2one(
        comodel_name='creativeflow.template.category',
        string="Category",
        required=True,
        ondelete='restrict'
    )
    tags_ids = fields.Many2many(
        comodel_name='creativeflow.template.tag',
        string="Tags"
    )
    preview_image_url = fields.Char(
        string="Preview Image URL",
        help="URL to the preview image, likely in MinIO S3 storage."
    )
    template_json_data = fields.Text(
        string="Template JSON Data",
        required=True,
        help="JSON structure defining the template elements and layout for the frontend editor."
    )
    is_active = fields.Boolean(
        string="Active",
        default=True,
        help="Whether this template is available to users on the platform."
    )
    platform_suitability = fields.Char(
        string="Platform Suitability",
        help="e.g., Instagram Post, Facebook Ad, comma-separated"
    )
    usage_count = fields.Integer(
        string="Usage Count",
        default=0,
        readonly=True,
        copy=False,
        help="How many times this template has been used."
    )
    is_pro_template = fields.Boolean(
        string="Pro Template",
        default=False,
        help="Check this if the template is restricted to Pro tier users and above."
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    def action_view_on_platform(self):
        """
        Placeholder method to open a preview of the template on the actual
        CreativeFlow platform. Requires a configured base URL.
        """
        self.ensure_one()
        # base_url = self.env['ir.config_parameter'].sudo().get_param('creativeflow.platform_base_url')
        # if base_url:
        #     return {
        #         'type': 'ir.actions.act_url',
        #         'url': f"{base_url}/templates/{self.id}",
        #         'target': 'new',
        #     }
        return True