# -*- coding: utf-8 -*-
from odoo import fields, models


class CreativeTemplateCategory(models.Model):
    """
    Model for categorizing creative templates. Supports hierarchical
    structure for better organization.
    """
    _name = 'creativeflow.template.category'
    _description = 'CreativeFlow Template Category'
    _parent_store = True
    _order = 'sequence, name'

    name = fields.Char(
        string="Category Name",
        required=True,
        translate=True
    )
    parent_id = fields.Many2one(
        comodel_name='creativeflow.template.category',
        string="Parent Category",
        ondelete='cascade',
        index=True
    )
    parent_path = fields.Char(index=True)
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determines the display order."
    )
    child_ids = fields.One2many(
        comodel_name='creativeflow.template.category',
        inverse_name='parent_id',
        string='Child Categories'
    )