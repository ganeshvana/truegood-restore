# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Header - Extended',
    'version' : '14.0.1.1',
	'author' : 'Oodu Implementers Private Limited',
    'summary': 'Inherit default Header',
    'description': """""",
    'category' : 'Report',
    'website': 'https://www.odooimplementers.com',
    'depends' : ['base','web','l10n_in'],
    'data': [
    'report/header.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
