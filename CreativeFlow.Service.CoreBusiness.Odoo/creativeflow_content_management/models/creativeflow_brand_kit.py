from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CreativeFlowBrandKit(models.Model):
    _name = 'creativeflow.brand_kit'
    _description = 'CreativeFlow Brand Kit'
    _order = 'is_default desc, name'

    name = fields.Char(string="Brand Kit Name", required=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        required=True,
        ondelete='cascade',
        default=lambda self: self.env.user
    )
    colors = fields.Text(
        string="Color Palette (JSON)",
        help="JSON string for color palette, e.g., '[{\"name\": \"Primary\", \"hex\": \"#FF0000\"}]'"
    )
    fonts = fields.Text(
        string="Fonts (JSON)",
        help="JSON string for font definitions, e.g., '[{\"name\": \"Heading\", \"family\": \"Arial\"}]'"
    )
    logos = fields.Text(
        string="Logos (JSON)",
        help="JSON string of logo asset MinIO paths, e.g., '[{\"name\": \"Main Logo\", \"path\": \"...\"}]'"
    )
    is_default = fields.Boolean(
        string="Is Default",
        default=False,
        copy=False,
        help="If checked, this brand kit will be the default for the user."
    )

    _sql_constraints = [
        ('unique_default_per_user', 'CHECK (1=1)', 'A user can only have one default brand kit. This is enforced programmatically.'),
    ]

    @api.constrains('is_default', 'user_id')
    def _check_single_default_brand_kit(self):
        """ Ensures a user doesn't have more than one default brand kit. """
        for kit in self:
            if kit.is_default:
                domain = [
                    ('user_id', '=', kit.user_id.id),
                    ('is_default', '=', True),
                    ('id', '!=', kit.id)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(_("You can only have one default brand kit per user."))

    @api.model_create_multi
    def create(self, vals_list):
        """ On creation, if a kit is set as default, unset the previous default. """
        for vals in vals_list:
            if vals.get('is_default') and vals.get('user_id'):
                self.env['creativeflow.brand_kit'].search([
                    ('user_id', '=', vals['user_id']),
                    ('is_default', '=', True)
                ]).write({'is_default': False})
        return super().create(vals_list)

    def write(self, vals):
        """ On write, if a kit is set as default, unset the previous default. """
        if 'is_default' in vals and vals['is_default']:
            for kit in self:
                self.search([
                    ('user_id', '=', kit.user_id.id),
                    ('is_default', '=', True),
                    ('id', '!=', kit.id)
                ]).write({'is_default': False})
        return super().write(vals)