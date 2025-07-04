{
    'name': "CreativeFlow Helpdesk",
    'version': "1.0.0",
    'summary': "Customizes Odoo Helpdesk for CreativeFlow customer support.",
    'description': """
        Leverages and extends Odoo's Helpdesk and Knowledge modules to provide a
        comprehensive customer support solution for CreativeFlow.
        - Adds custom fields to tickets for better context.
        - Configures default teams and stages for the support workflow.
    """,
    'author': "CreativeFlow",
    'website': "https://www.creativeflow.com",
    'category': "CreativeFlow/Support",
    'depends': [
        'helpdesk',
        'website_helpdesk',
        'knowledge',
        'creativeflow_core'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/helpdesk_team_data.xml',
        'views/helpdesk_views_extension.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}