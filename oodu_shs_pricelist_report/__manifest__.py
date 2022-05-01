# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Pricelist Report',
    "version": "14.1.0.0",
    'summary': 'Pricelist Report',
    'description': """Pricelist Report""",
    'author' : "Oodu Implementers Pvt Ltd",
    'website': "www.odooimplementers.com",
    'category': 'Inventory',
    'depends': ['base', 'stock'],
    'data': [
    'views/stock_view.xml',
    'views/pricelist_report_view.xml',
    'views/pricelist_template_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
