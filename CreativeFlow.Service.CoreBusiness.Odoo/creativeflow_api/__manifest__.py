{
    'name': 'CreativeFlow AI - REST API',
    'version': '18.0.1.0.0',
    'summary': 'Provides the RESTful API endpoints for the CreativeFlow platform.',
    'author': 'CreativeFlow Inc.',
    'website': 'https://www.creativeflow.ai',
    'category': 'Creative/AI',
    'depends': [
        'creativeflow_base',
        'creativeflow_content_management',
        'creativeflow_billing_subscription',
        'creativeflow_integration_rabbitmq',
        'web', # dependency for http controllers
    ],
    'data': [],
    'installable': True,
    'license': 'OEEL-1',
}