# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BrandKit(models.Model):
    """
    Represents a CreativeFlow Brand Kit, a collection of brand assets and
    preferences owned by a user or team.
    """
    _name = 'creativeflow.brand.kit'
    _description = 'CreativeFlow Brand Kit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Owner",
        required=True,
        index=True,
        default=lambda self: self.env.user
    )
    cf_team_id_external = fields.Char(
        string="CreativeFlow Team ID (External)",
        help="External ID of the team owning this brand kit, if applicable."
    )
    colors_json = fields.Text(
        string="Colors (JSON)",
        help="JSON string representing color palettes. E.g., [{'name': 'Primary', 'hex': '#FF0000'}]"
    )
    fonts_json = fields.Text(
        string="Fonts (JSON)",
        help="JSON string representing font definitions. E.g., [{'name': 'Heading', 'family': 'Arial'}]"
    )
    logo_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='creativeflow_brand_kit_logo_rel',
        column1='brand_kit_id',
        column2='attachment_id',
        string="Logos",
        help="Upload company logos and other key brand imagery."
    )
    style_preferences_json = fields.Text(
        string="Style Preferences (JSON)",
        help="JSON object representing brand style preferences like tone, mood, etc."
    )
    is_default_for_user = fields.Boolean(
        string="Default Brand Kit for User",
        help="If checked, this brand kit will be the default for the owner."
    )
    cf_external_brand_kit_id = fields.Char(
        string="CreativeFlow Brand Kit ID (External)",
        index=True,
        copy=False
    )

    @api.constrains('user_id', 'is_default_for_user')
    def _check_unique_default_for_user(self):
        """
        Ensures that a user can only have one default brand kit.
        """
        for brand_kit in self.filtered('is_default_for_user'):
            domain = [
                ('id', '!=', brand_kit.id),
                ('user_id', '=', brand_kit.user_id.id),
                ('is_default_for_user', '=', True)
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_('A user can only have one default brand kit. Please uncheck the default setting on other brand kits for this user.'))