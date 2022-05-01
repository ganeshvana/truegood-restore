from odoo import api, fields, models
import logging
import requests, json

_logger = logging.getLogger(__name__)


class saleordered(models.Model):
	_inherit = "sale.order"

	commitment_date = fields.Datetime('Commitment Date',
			        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
			        copy=False, oldname='requested_date', readonly=False,
			        help="This is the delivery date promised to the customer. If set, the delivery order "
			             "will be scheduled based on this date rather than product lead times.")
