{
    'name': "CreativeFlow Template Catalog",
    'version': "1.0.0",
    'summary': "Manages the creative template catalog for CreativeFlow AI.",
    'description': """
        Provides an administrative interface within Odoo to manage the library
        of creative templates offered on the CreativeFlow platform. This includes
        models for templates, categories, and tags, along with the necessary
        views and access controls.
    """,
    'author': "CreativeFlow",
    'website': "https://www.creativeflow.com",
    'category': "CreativeFlow/Content Management",
    'depends': [
        'base',
        'creativeflow_core'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/template_category_data.xml',
        'views/template_category_views.xml',
        'views/template_tag_views.xml',
        'views/template_views.xml',
        'views/template_catalog_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}