# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Report Extended',
    'version': '14.0.1.0',
    'author': 'Oodu Implementers Private Limited',
    'website': 'https://www.odooimplementers.com',
    'category': 'Sale',
    'summary': 'Sale Report Extended',
    'description': """Sale Report Extended""",
    'depends': ['base', 'sale', 'product', 'account'],
    'data': [
    'security/ir.model.access.csv',
    'views/partner_views.xml',
    # 'views/sale_template_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
