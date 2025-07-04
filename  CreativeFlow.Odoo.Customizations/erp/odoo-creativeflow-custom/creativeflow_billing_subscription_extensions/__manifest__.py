# -*- coding: utf-8 -*-
{
    'name': "CreativeFlow Billing & Subscription Extensions",
    'version': "18.0.1.0.0",
    'summary': "Extends Odoo subscription management for CreativeFlow specific logic.",
    'category': "CreativeFlow/Billing",
    'author': "CreativeFlow AI Team",
    'website': "https://creativeflow.ai",
    'depends': [
        'sale_subscription',
        'creativeflow_user_extensions',
        'creativeflow_credits'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_subscription_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}