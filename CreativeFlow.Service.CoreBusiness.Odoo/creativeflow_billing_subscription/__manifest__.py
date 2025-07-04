{
    'name': 'CreativeFlow AI - Billing & Subscriptions',
    'version': '18.0.1.0.0',
    'summary': 'Manages subscription plans, payments, and the credit system.',
    'author': 'CreativeFlow Inc.',
    'website': 'https://www.creativeflow.ai',
    'category': 'Creative/AI',
    'depends': [
        'creativeflow_base',
        'sale_subscription',
        'account',
        'payment',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'views/subscription_views.xml',
        'views/credit_transaction_views.xml',
    ],
    'installable': True,
    'license': 'OEEL-1',
}