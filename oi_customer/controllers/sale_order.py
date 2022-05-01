# -*- coding: utf-8 -*-

import json
from datetime import datetime
from .token import has_valid_token
from odoo.http import Controller, Response, request, route


class CategoryApi(Controller):

    @route('/saleorder/create', type="json", auth='public', methods=["POST"], csrf=False)
    @has_valid_token
    def create_sale_order(self):
        data = request.jsonrequest
        api_tracker = request.env['oi.api.tracker'].sudo().create({
            'name': '/saleorder/create',
            'request_body': data,
            'response': ''
        })
        if data:
            sale = request.env['sale.order']
            order_lines = []
            for line in data.get('order_line'):
                # if 'tax_id' in line:
                #     tax_obj = request.env['account.tax'].sudo().search([('amount', '=', line.get('tax_id'))], limit=1)
                #     if tax_obj:
                #         line.update({
                #             'tax_id': [(6, 0, [tax_obj.id])]
                #         })
                #     else:
                #         return {"message": "The Tax Given in the request does not exist in the system !"}
                if 'product_id' in line:
                    product_obj = request.env['product.product'].sudo().search([('id', '=', line.get('product_id'))], limit=1)
                    if product_obj:
                        line.update({
                            'product_id': product_obj.id
                        })
                    else:
                        return {"message": "The Product Id Given in the request does not exist in the system !"}
                order_lines.append((0, 0, line))
            if data.get('delivery_charge'):
                product_id = request.env['product.product'].sudo().search([('default_code', '=', 'Delivery_Charge')])
                delivery_line = {
                    "product_id": product_id.id,
                    "product_uom_qty": 1,
                    "price_unit": int(data.get('delivery_charge')),
                    "price_subtotal": int(data.get('delivery_charge'))
                }
                order_lines.append((0, 0, delivery_line))

            customer = request.env["res.partner"].sudo().search([('mobile_ref', '=', data.get('partner_id'))], limit=1)
            delivery_address = request.env["res.partner"].sudo().search([('mobile_ref', '=', data.get('partner_shipping_id'))], limit=1)
            if customer and delivery_address:

                # if data.get('expected_delivery'):
                #     date = datetime.strptime(data.get('expected_delivery'), "%d/%m/%Y")
                # else:
                #     date = False
                order_data = {
                    'partner_id': customer.id,
                    'partner_shipping_id': delivery_address.id,
                    'partner_invoice_id': customer.id,
                    'delivery_slot': data.get('delivery_slot'),
                    'payment_mode': data.get('payment_mode'),
                    # 'commitment_date': date,
                    'order_line': order_lines
                }
                order = sale.sudo().create(order_data)
                order.action_confirm()
                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "SALE",
                        "message": "Sale Order Created Successfully.",
                        "payload": order.name}
            else:
                return {"message": "The requested customer is not present !"}
        else:
            return {"message": "There is no data in the request !"}

    @route('/saleorder/cancel', type="json", auth='public', methods=["POST"], csrf=False)
    @has_valid_token
    def cancel_sale_order(self):
        data = request.jsonrequest
        if data:
            order = request.env["sale.order"].sudo().search([('name', '=', data.get('order_id'))], limit=1)
            if order:
                order.sudo().action_cancel()
                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "SALE",
                        "message": "Sale Order Cancelled Successfully.",
                        "payload": order.name}
            else:
                return {"message": "Order not found !"}
        else:
            return {"message": "empty request !"}

    @route('/saleorder/getStatusById', type="json", auth='public', methods=["GET"], csrf=False)
    @has_valid_token
    def get_order_status_byid(self):
        data = request.jsonrequest
        if data:
            order = request.env["sale.order"].sudo().search([('name', '=', data.get('order_id'))], limit=1)
            if order:
                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "Sale",
                        "message": "Sale Order Status.",
                        "payload":
                            {
                                "order_status": order.state
                            }
                        }
            else:
                return {"message": "Sale Order With this ID does not exist !"}
        else:
            return {"message": "Empty Request !"}
