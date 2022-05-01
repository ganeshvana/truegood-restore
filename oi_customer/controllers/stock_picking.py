# -*- coding: utf-8 -*-

from .token import has_valid_token
from odoo.http import Controller, Response, request, route


class StockPicking(Controller):

    @route('/delivery/statusUpdate', type="json", auth='public', methods=["POST"], csrf=False)
    @has_valid_token
    def update_delivery_status(self):
        data = request.jsonrequest
        sale_order = request.env["sale.order"].sudo().search([('name', '=', data.get('order_id'))], limit=1)
        if sale_order:
            sale_order.sudo().write({
                'mobile_delivery_status': data.get('delivery_status')
            })
            related_pickings = sale_order.picking_ids
            delivery_order = related_pickings.filtered(lambda p: 'OUT' in p.name)
            if delivery_order:
                delivery_order.sudo().write({
                    'mobile_delivery_status': data.get('delivery_status')
                })
                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "Delivery",
                        "message": "Delivery Status Updated Successfully.",
                        "payload": sale_order.name}
            else:
                return {"message": "Delivery Order not Found"}
        else:
            return {"message": "Sale Order not Found"}
