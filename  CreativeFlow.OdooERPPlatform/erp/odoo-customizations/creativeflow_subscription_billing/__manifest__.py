{
    'name': "CreativeFlow Subscription & Billing",
    'version': "1.0.0",
    'summary': "Manages subscriptions, billing, credits, and payment integration for CreativeFlow.",
    'description': """
        Handles all aspects of subscription and billing for the CreativeFlow platform within Odoo.
        - Manages subscription plans as Odoo products.
        - Integrates with Stripe and PayPal via webhooks.
        - Implements a credit management system for users.
        - Extends subscriptions to handle credit allotments and platform synchronization.
    """,
    'author': "CreativeFlow",
    'website': "https://www.creativeflow.com",
    'category': "CreativeFlow/Billing",
    'depends': [
        'sale_subscription',
        'account',
        'payment',
        'creativeflow_core'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_acquirer_data.xml',
        'data/subscription_product_data.xml',
        'views/creativeflow_credit_log_views.xml',
        'views/subscription_views.xml',
        'views/billing_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}