# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Report Calls Product',
    'version': '14.0.1.0',
    'author': 'Oodu Implementers Private Limited',
    'website': 'https://www.odooimplementers.com',
    'category': 'Purchase',
    'summary': 'Purchase Report Calls Product Name',
    'description': """Purchase Report Calls Product Name""",
    'depends': ['base', 'purchase'],
    'data': [
     'views/purchase_quotation_report.xml',
    ],
    'installable': True,
    'auto_install': False
}
