# -*- coding: utf-8 -*-

import json
from .token import has_valid_token
from odoo.http import Controller, Response, request, route


class SalesPriceList(Controller):

    @route('/getPricelists', type="json", auth='public', methods=["POST"], csrf=False)
    @has_valid_token
    def get_all_pricelist(self):
        pricelists = request.env['product.pricelist'].sudo().search([])
        if pricelists:
            pricelist_list = []
            for pricelist in pricelists:
                details = {
                    'pricelist_id': pricelist.id,
                    'pricelist_name': pricelist.name,
                    'pricelist_items': [{
                        'product_id': item.product_tmpl_id.product_variant_ids.id,
                        'product_name': item.product_tmpl_id.product_variant_ids.name,
                        'computation_method': item.compute_price,
                        'discount_percent': item.percent_price,
                        'fixed_price': item.fixed_price,
                    } for item in pricelist.item_ids]
                }
                pricelist_list.append(details)

            return {"session_valid": True,
                    "response_code": 200,
                    "status": "success",
                    "message_code": "PRICELIST",
                    "message": "Pricelist List.",
                    "payload": pricelist_list}
        else:
            return {"message": "There is no pricelist found !"}
