# -*- coding: utf-8 -*-
{
    'name': "CreativeFlow Brand Kit & Workbench Management",
    'version': "18.0.1.0.0",
    'summary': "Basic Odoo models for CreativeFlow Brand Kits and Workbenches.",
    'category': "CreativeFlow/Content Management",
    'author': "CreativeFlow AI Team",
    'website': "https://creativeflow.ai",
    'depends': [
        'base',
        'mail',
        'attachment_indexation',
        'creativeflow_user_extensions'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/creativeflow_brand_workbench_security.xml',
        'views/brand_kit_views.xml',
        'views/workbench_views.xml',
        'views/brand_workbench_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}