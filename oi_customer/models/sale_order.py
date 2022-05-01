# -*- coding: utf-8 -*-

import requests
import logging
from ast import literal_eval
from .auth_token import get_authentication_token

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_slot = fields.Char(string="Delivery Slot")
    mobile_delivery_status = fields.Selection(selection=[
        ('ready', 'Ready'),
        ('pick', 'Picked'),
        ('delivery', 'Delivered'),
        ('hold', 'Hold'),
        ('return', 'Delivered'),
    ], string='Mobile Delivery Status', readonly=True, copy=False, tracking=True,
        default='ready')
    payment_mode = fields.Selection(selection=[
        ('prepaid', 'Prepaid'),
        ('cod', 'Cash On Delivery'),
    ], string='Payment Mode', readonly=True, copy=False, tracking=True)
    delivery_status = fields.Selection([
        ('in_progress', 'In Progress'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ], string='Delivery Status', copy=False, tracking=True,
        default='in_progress')

    def update_status_to_mobile_app(self):
        if self.delivery_status == 'delivered':
            base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
            jwt_token = get_authentication_token(base_url=base_url)
            headers = {'x-auth-token': jwt_token,
                       'content-type': 'application/json'}
            body = {
                'order_status': 'delivered',
                'delivery_status': 'delivered',
            }

            url = base_url + '/order/edit/' + str(self.name)
            r = requests.put(url, json=body, headers=headers, timeout=30)

            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': body,
                'response': result
            })
            _logger.info("Order status updated to mobile app %s" % result)
        else:
            raise UserError("This order Status is already updated !")

class Partner(models.Model):
    _inherit = 'res.partner'

    delivery_address_type = fields.Char("Delivery Address Type")
