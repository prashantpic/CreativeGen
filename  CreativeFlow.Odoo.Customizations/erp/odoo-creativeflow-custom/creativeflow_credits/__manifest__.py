# -*- coding: utf-8 -*-
{
    'name': "CreativeFlow Credit System",
    'version': "18.0.1.0.0",
    'summary': "Manages user credits, action costs, and credit transactions for the CreativeFlow platform.",
    'category': "CreativeFlow/Billing",
    'author': "CreativeFlow AI Team",
    'website': "https://creativeflow.ai",
    'depends': ['base', 'mail', 'creativeflow_user_extensions'],
    'data': [
        'security/ir.model.access.csv',
        'views/credit_transaction_views.xml',
        'views/credit_action_cost_views.xml',
        'views/res_users_credit_views.xml',
        'views/credit_menus.xml',
        'data/credit_action_cost_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}