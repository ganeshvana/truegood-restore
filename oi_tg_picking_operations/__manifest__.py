# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Picking Operations - Extended',
    "version": "14.0.1.0.0",
    'summary': 'Picking Operations - Extended',
    'author': 'Oodu Implementers Pvt Ltd.',
    'description': """Picking Operations Report""",
    'category': 'Inventory',
    'depends': ['base', 'stock'],
    'data': [
    # 'views/purchase_view.xml',
    'views/stock_report_extend.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
