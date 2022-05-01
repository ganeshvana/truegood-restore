from odoo import api, fields, models, _


class stock_picking(models.Model):
    _inherit = "stock.picking"
    
    
    pricelist_id = fields.Many2one(
            'product.pricelist', string='Pricelist', check_company=True,  default=1,# Unrequired company
            required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
            domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")    

