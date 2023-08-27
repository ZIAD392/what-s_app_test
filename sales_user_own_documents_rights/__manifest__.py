{
    'name': 'Sales User Own Documents Rights',
    'author': "Mohamed",
    'version': '16.0.0',
    'category': 'sales',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'sales_team',
        'sale_margin',
        'crm',
    ],
    'data': [
        'security/project_coordinator_security.xml',
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/crm_lead.xml',
        'views/customs_group_actions.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
