from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class accinherit(models.Model):
    _inherit = "account.payment"
    Cheque  = fields.Float(string='Cheque No')

   	