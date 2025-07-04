# -*- coding: utf-8 -*-
{
    'name': "CreativeFlow User Extensions",
    'version': "18.0.1.0.0",
    'summary': "Extends Odoo users with CreativeFlow specific fields like credit balance and subscription tier.",
    'category': "CreativeFlow/User Management",
    'author': "CreativeFlow AI Team",
    'website': "https://creativeflow.ai",
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}