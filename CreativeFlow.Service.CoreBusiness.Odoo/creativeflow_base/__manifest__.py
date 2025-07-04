{
    'name': 'CreativeFlow AI - Base Module',
    'version': '18.0.1.0.0',
    'summary': 'Core models and base functionality for the CreativeFlow AI platform.',
    'author': 'CreativeFlow Inc.',
    'website': 'https://www.creativeflow.ai',
    'category': 'Creative/AI',
    'depends': [
        'base',
        'web',
        'auth_signup',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/creativeflow_menus.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OEEL-1',
}