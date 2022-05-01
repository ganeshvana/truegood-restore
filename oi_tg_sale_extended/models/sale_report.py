from odoo import fields, models, api
from odoo import tools

class SaleReport(models.Model):
    _inherit = 'sale.report'

    customer_type_id = fields.Many2one('customer.type', "Customer Type")
    customer_source_id = fields.Many2one('customer.source', "Customer Source")
    standard_price = fields.Float("Cost Price")
    ref = fields.Char(string="Customer Reference")
    actual_delivery_date = fields.Date("Actual Delivery Date")
    commitment_date = fields.Date("Planned Delivery Date")
    
    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['actual_delivery_date'] = ', s.actual_delivery_date as actual_delivery_date'
        fields['customer_type_id'] = ', partner.customer_type_id as customer_type_id'
        fields['customer_source_id'] = ', partner.customer_source_id as customer_source_id'
        fields['commitment_date'] = ', s.commitment_date as commitment_date'
        fields['ref'] = ', partner.ref as ref'
        fields['standard_price'] = ', sum(t.standard_price * l.product_uom_qty / u.factor * u2.factor) as standard_price'
        

        groupby += ', s.invoice_status,partner.customer_type_id,partner.customer_source_id,partner.commercial_partner_id,partner.ref,t.standard_price,l.product_uom_qty'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

#     def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
#         res = super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
# 
#         select_ = """
#             coalesce(min(l.id), -s.id) as id,           
#             s.actual_delivery_date as actual_delivery_date,
#             s.commitment_date as commitment_date,            
#             partner.customer_type_id as customer_type_id,
#             partner.customer_source_id as customer_source_id,
#             partner.ref as ref,
#             
#         """
# 
#         for field in fields.keys():
#             select_ += ', NULL AS %s' % (field)
# 
#         from_ = """
#                 sale_order_line l
#                       right outer join sale_order s on (s.id=l.order_id)
#                       join res_partner partner on s.partner_id = partner.id
#                         left join product_product p on (l.product_id=p.id)
#                             left join product_template t on (p.product_tmpl_id=t.id)
#                     left join uom_uom u on (u.id=l.product_uom)
#                     left join uom_uom u2 on (u2.id=t.uom_id)
#                     left join product_pricelist pp on (s.pricelist_id = pp.id)
#                 
#         """ 
# 
#         groupby_ = """
#             l.product_id,
#             l.order_id,
#             t.uom_id,
#             t.categ_id,
#             s.name,
#             s.date_order,
#             s.partner_id,
#             s.user_id,
#             s.state,
#             s.company_id,
#             s.campaign_id,
#             s.medium_id,
#             s.source_id,
#             s.pricelist_id,
#             s.analytic_account_id,
#             s.team_id,
#             p.product_tmpl_id,
#             partner.country_id,
#             partner.industry_id,
#             partner.customer_type_id,
#             partner.customer_source_id,
#             partner.commercial_partner_id,
#             partner.ref,
#             l.discount,
#             s.id
#         """ 
# 
#         current = '(SELECT %s FROM %s GROUP BY %s)' % (select_, from_, groupby_)
# 
#         return '%s UNION ALL %s' % (res, current)

# class SaleOrderReportProforma(models.AbstractModel):
#     _name = 'report.sale.report_saleproforma'
#     _description = 'Proforma Report'
# 
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['sale.order'].browse(docids)
#         return {
#             'doc_ids': docs.ids,
#             'doc_model': 'sale.order',
#             'docs': docs,
#             'proforma': True
#         }
