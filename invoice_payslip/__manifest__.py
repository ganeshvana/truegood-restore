# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'invoice pay_slip',
    'version': '1.0',
    'category': 'invoice_payslip',
    'summary': 'invoice_payslip',
    'description': "",
    'website': 'https://www.odooimplementers.com',
    'depends': ['sale', 'account'],
    'data': [
        'reports/invoice_template.xml',
        'reports/invoices.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
