{
    'name': 'CreativeFlow AI - Helpdesk Customizations',
    'version': '18.0.1.0.0',
    'summary': 'Customizes the Helpdesk module for CreativeFlow needs.',
    'author': 'CreativeFlow Inc.',
    'website': 'https://www.creativeflow.ai',
    'category': 'Creative/AI',
    'depends': [
        'creativeflow_base',
        'creativeflow_content_management', # For relations to project/generation
        'helpdesk',
        'website_helpdesk_form',
    ],
    'data': [
        'views/helpdesk_ticket_views.xml',
    ],
    'installable': True,
    'license': 'OEEL-1',
}