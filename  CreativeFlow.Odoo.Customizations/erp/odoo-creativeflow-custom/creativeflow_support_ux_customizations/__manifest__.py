# -*- coding: utf-8 -*-
{
    'name': "CreativeFlow Support UX Customizations",
    'version': "18.0.1.0.0",
    'summary': "Customizes Odoo Helpdesk & Knowledge modules for CreativeFlow branding and UX.",
    'category': "CreativeFlow/Support",
    'author': "CreativeFlow AI Team",
    'website': "https://creativeflow.ai",
    'depends': [
        'helpdesk',
        'knowledge',
        'website'
    ],
    'data': [
        'views/helpdesk_ticket_views.xml',
        'views/knowledge_article_views.xml',
        'views/support_portal_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'creativeflow_support_ux_customizations/static/src/scss/creativeflow_branding.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}