# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Inward Serial Number',
    'version' : '1.1',
    'summary': 'Inventory',
    'sequence': 10,
    'description': """
        Button to create automatic Inward Serial Number
    """,
    'category': 'Inventory',
    'website': '',
    'depends' : ['purchase', 'stock'],
    'data': [
        
        'views/detailed_operations_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
