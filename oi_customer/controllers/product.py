# -*- coding: utf-8 -*-

import json
from .token import has_valid_token
from odoo.http import Controller, Response, request, route


class ProductsApi(Controller):

    @route('/getAllProduct', type="json", auth='public', methods=["GET"], csrf=False)
    @has_valid_token
    def get_product(self):
        products = request.env['product.product'].sudo().search([])
        if products:
            product_list = []
            for product in products:
                details = {
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_imgurl': '',
                    'product_price': product.lst_price,
                    'product_weight': '',
                    'product_discount': '',
                    'product_description': product.description_sale,
                    'product_category': product.categ_id.name,
                    'product_uom': product.uom_id.name,
                    'product_taxes': [tax.amount for tax in product.taxes_id],
                    'search_keywords': [keyword.name for keyword in product.keyword_search]
                }
                product_list.append(details)

            return {"session_valid": True,
                    "response_code": 200,
                    "status": "success",
                    "message_code": "PRODUCT",
                    "message": "Product List.",
                    "payload": product_list}
        else:
            return {"message": "There are no products found !"}

    @route('/subcategory/products', type="json", auth='public', methods=["GET"], csrf=False)
    @has_valid_token
    def get_subcategory_product_list(self):
        data = request.jsonrequest
        if data:
            category_id = int(data.get('category_id'))
            if category_id:
                # categ_obj = request.env['product.category'].sudo().browse(category_id)
                products = request.env['product.product'].sudo().search([('app_subcategory', '=', category_id)])
                if products:
                    product_list = []
                    for product in products:
                        product_list.append({
                            'product_id': product.id,
                            'product_name': product.name,
                            'product_imgurl': '',
                            'product_price': product.lst_price,
                            'product_weight': '',
                            'product_discount': '',
                            'product_description': product.description_sale,
                            'product_category': product.categ_id.name,
                            'product_uom': product.uom_id.name,
                            'product_taxes': [tax.amount for tax in product.taxes_id],
                            'search_keywords': [keyword.name for keyword in product.keyword_search]

                        })

                    return {"session_valid": True,
                            "response_code": 200,
                            "status": "success",
                            "message_code": "PRODUCT",
                            "message": "Product List Under a specific category.",
                            "payload": product_list}
                else:
                    return {"message": "There are no products for this category !"}
            else:
                return {"message": "There are no category in this id !"}
