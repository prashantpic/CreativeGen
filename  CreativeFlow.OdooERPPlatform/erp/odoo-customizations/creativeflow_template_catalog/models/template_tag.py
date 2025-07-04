# -*- coding: utf-8 -*-
from odoo import fields, models


class CreativeTemplateTag(models.Model):
    """
    Model for creating tags that can be assigned to creative templates
    to facilitate searching and filtering.
    """
    _name = 'creativeflow.template.tag'
    _description = 'CreativeFlow Template Tag'
    _order = 'name'

    name = fields.Char(
        string="Tag Name",
        required=True,
        translate=True
    )
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name must be unique!"),
    ]