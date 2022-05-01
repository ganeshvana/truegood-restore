# -*- coding: utf-8 -*-
{
    'name': "Customer API's",
    'summary': """
        The module helps creating/updating customers from external applications through API""",
    'description': """
        The module helps creating/updating customers from external applications through API
    """,
    'author': "Muhsin, Odoo Implementors",
    'website': "http://www.odooimplementers.com/",
    'category': 'Uncategorized',
    'version': '14.0.1',

    'depends': ['base',
                'sale',
                'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/api_user_data.xml',
        'data/api_url_data.xml',
        'views/res_users_views.xml',
        'views/res_partner.xml',
        'views/product_view.xml',
        'views/account_move_view.xml',
        'views/mobile_app_category_view.xml',
        'views/oi_api_tracker_views.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
    ],
}
