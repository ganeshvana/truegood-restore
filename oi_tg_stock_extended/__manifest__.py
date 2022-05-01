# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Invoice Creation from Picking',
    'version': '14.0.1.0',
    'author': 'Oodu Implementers Private Limited',
    'website': 'https://www.odooimplementers.com',
    'category': 'Stock',
    'summary': 'Creation of Invoice from picking',
    'description': """This module allows to create draft invoice on validating delivery order""",
    'depends': ['base', 'stock', 'sale'],
    'data': [
    'views/stock_picking_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
