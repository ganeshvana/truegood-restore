# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

    
class res_partner(models.Model):
    _inherit = 'res.partner'
    # _rec_name = 'name'
    
    customer_type_id = fields.Many2one('customer.type', "Customer Type")
    customer_source_id = fields.Many2one('customer.source', "Customer Source")
    
    @api.onchange('ref')
    def onchange_ref(self):
        if self.ref:
            if len(data) != 10:                
                raise UserError(_("Reference should be 10 digits."))

    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''
            street = partner.street or ''
            city = partner.city or ''
            res.append((partner.id, name + "-" + street + "-" + city))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(res_partner, self).create(vals_list)
        if res.ref:
            data = str(res.ref)
            if len(data) != 10:                
                raise UserError(_("Reference should be 10 digits."))
        return res
    
#     def write(self, vals):
#         res = super(res_partner, self).write(vals)
#         if self.ref:
#             if len(data) != 10:                
#                 raise UserError(_("Reference should be 10 digits."))
#         return res
    
class CustomerType(models.Model):
    _name = 'customer.type'
    _description = 'Customer Type'
    
    name = fields.Char("Type")
    
class CustomerSource(models.Model):
    _name = 'customer.source'
    _description = 'Customer Source'
    
    name = fields.Char("Source")
    
class Sale(models.Model):
   _inherit = 'sale.order'
   
   customer_ref = fields.Char(related='partner_id.ref', string="Customer Reference#")
   actual_delivery_date = fields.Date("Actual Delivery Date")
   
class Sale(models.Model):
   _inherit = 'product.template'
   _order = 'product_weight'
   
   standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits='Product Price', groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
        In FIFO: value of the last unit that left the stock (automatically computed).
        Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
        Used to compute margins on sale orders.""", store=True)
   product_weight = fields.Selection([('1', 'Heaviest'),('2', 'Heavy'),('3', 'Medium'),('4','Light'),('5', 'Lightest')], "Weight Category")
 
class AML(models.Model):
   _inherit = 'account.move.line'
   _order = 'product_weight, name'
   
   product_weight = fields.Selection(related='product_id.product_weight')
   
class SOL(models.Model):
   _inherit = 'sale.order.line'
   _order = 'product_weight, name'
   
   product_weight = fields.Selection(related='product_id.product_weight')
   
   