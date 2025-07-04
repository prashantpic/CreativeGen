{
    'name': 'CreativeFlow AI - Content Management',
    'version': '18.0.1.0.0',
    'summary': 'Manages Workbenches, Projects, Brand Kits, and other creative content.',
    'author': 'CreativeFlow Inc.',
    'website': 'https://www.creativeflow.ai',
    'category': 'Creative/AI',
    'depends': [
        'creativeflow_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/creativeflow_brand_kit_views.xml',
        'views/creativeflow_workbench_views.xml',
        'views/creativeflow_project_views.xml',
        'views/creativeflow_generation_request_views.xml',
        'views/content_management_menus.xml',
    ],
    'installable': True,
    'license': 'OEEL-1',
}