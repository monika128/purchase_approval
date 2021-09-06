# -*- coding: utf-8 -*-
{
    'name': "Purchase Approval",

    'summary': """
        Extending Default approval for PO without manager Acceess""",

    'description': """ Extended Purchase Approvals
    """,

    'author': "Monika",
    'website': "www.linkedin.com/in/monika-phadtare-python-dev",

    'category': 'Purchases',
    'version': '12.1',

    'depends': ['base','purchase','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/purchase_res_config.xml',
    ],
}