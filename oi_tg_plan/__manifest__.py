# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'planned',
    'version': '14.0.1.0',
    'sequence': -100,
    'author': 'Oodu Implementers Private Limited',
    'website': 'https://www.odooimplementers.com',
    'category': 'Sale',
    'summary': 'Sale Report Extended',
    'description': """Sale Report Extended""",
    'depends': ['sale', 'product'],
    'data': [
    'views/saleinherit.xml',
    ],
    'installable': True,
    'auto_install': False
}
