{
    'name': "CreativeFlow Core Extensions",
    'version': "1.0.0",
    'summary': "Core extensions for CreativeFlow integration with Odoo.",
    'description': """
        This module provides core extensions and utilities shared across other
        CreativeFlow Odoo modules. It extends the res.partner model to include
        fields for displaying synced data from the main CreativeFlow platform.
    """,
    'author': "CreativeFlow",
    'website': "https://www.creativeflow.com",
    'category': "CreativeFlow/Core",
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views_extension.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}