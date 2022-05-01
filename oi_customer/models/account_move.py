# -*- coding: utf-8 -*-

import requests
import logging
from ast import literal_eval

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import config, misc, ustr

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    delivery_status = fields.Boolean("Delivery Status")

    def update_delivery_status_mobile_app(self):
        if self.delivery_status:
            raise ValidationError("delivery status already updated to mobile app !")
        else:
            base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
            order_id = ''
            for line in self.invoice_line_ids:
                order_id = line.sale_line_ids.order_id.id
                continue
            url = base_url + '/order/' + str(order_id)
            arguments = {}
            r = requests.put(url, json=arguments, timeout=30)
            result = literal_eval(r.text)
            _logger.info("Delivery Status updated to mobile app %s" % result)
            self.delivery_status = True
