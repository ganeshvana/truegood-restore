# -*- coding: utf-8 -*-

import requests
import logging
from ast import literal_eval
from .auth_token import get_authentication_token

from odoo import fields, models, api

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    mobile_delivery_status = fields.Selection(selection=[
        ('ready', 'Ready'),
        ('pick', 'Picked'),
        ('delivery', 'Delivered'),
        ('hold', 'Hold'),
        ('return', 'Delivered'),
    ], string='Delivery Status', readonly=True, copy=False, tracking=True,
        default='ready')

    def action_assign(self):
        res = super(StockPicking, self).action_assign()

        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'content-type': 'application/json'}

        for line in self.move_ids_without_package:
            item_stock = line.product_id.qty_available - line.forecast_availability
            details = {
                'item_stock': str(item_stock)
            }

            url = base_url + '/product/' + str(line.product_id.id)
            r = requests.put(url, json=details, headers=headers, timeout=30)

            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': details,
                'response': result
            })
            _logger.info("Product Stock updated to mobile app %s" % result)

        return res

    def button_validate(self):

        res = super(StockPicking, self).button_validate()

        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'content-type': 'application/json'}
        if self.sale_id:
            self.sale_id.delivery_status = 'shipped'
            body = {
                'order_status': 'shipped',
                'delivery_status': 'shipped',
            }

            url = base_url + '/order/edit/' + str(self.sale_id.name)
            r = requests.put(url, json=body, headers=headers, timeout=30)

            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': body,
                'response': result
            })
            _logger.info("Order status updated to mobile app %s" % result)

        return res

    def action_cancel(self):
        res = super(StockPicking, self).action_cancel()

        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'content-type': 'application/json'}

        for line in self.move_ids_without_package:
            item_stock = line.product_id.qty_available - line.forecast_availability
            details = {
                'item_stock': str(item_stock)
            }

            url = base_url + '/product/' + str(line.product_id.id)
            r = requests.put(url, json=details, headers=headers, timeout=30)

            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': details,
                'response': result
            })
            _logger.info("Product Stock updated to mobile app %s" % result)

        return res

    def do_unreserve(self):
        res = super(StockPicking, self).do_unreserve()

        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'content-type': 'application/json'}

        for line in self.move_ids_without_package:
            item_stock = line.product_id.qty_available - line.forecast_availability
            details = {
                'item_stock': str(item_stock)
            }

            url = base_url + '/product/' + str(line.product_id.id)
            r = requests.put(url, json=details, headers=headers, timeout=30)

            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': details,
                'response': result
            })
            _logger.info("Product Stock updated to mobile app %s" % result)

        return res


