# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.import xlwt
import io
from io import StringIO
import base64
from io import BytesIO

import time
import xlwt
from datetime import datetime, date, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _, exceptions
from odoo.tools import date_utils
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class OrderReport(models.Model):
    _name = 'order.report'

   
    # partner_id = fields.Many2one('res.partner', string="Customer")
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)



    def get_data(self):
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        # workbook = xlwt.Workbook()
        title_format = workbook.add_format(
            {'font_name': 'TimesNew Roman', 'font_size': 11, 'align': 'center','bold': 1})
        row_header_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'bold': 1,
             'align': 'center'})
        align_right = workbook.add_format(
            {'align': 'right'})
        align_left = workbook.add_format(
            {'align': 'left'})
        row_format = workbook.add_format(
            {'font_size': 10})
        row_format.set_text_wrap()
        row_date_count = 7

        customers = []
        worksheet = workbook.add_worksheet('Order Report')

        worksheet.merge_range(0,0,0,4,'True Good Essentials',title_format)
        worksheet.merge_range(2,2,5,7,'Order Report',title_format)
        worksheet.write(row_date_count, 0, "Name", title_format)
        worksheet.write(row_date_count, 1, "Reference.", title_format)
        worksheet.write(row_date_count, 2, "Customer Source", title_format)
        worksheet.write(row_date_count, 3, "First Order Date", title_format)
        worksheet.write(row_date_count, 4, "Total Orders", title_format)
        worksheet.write(row_date_count, 5, "Latest Order Date", title_format)
        worksheet.write(row_date_count, 6, "Days Since Last Order", title_format)
        worksheet.write(row_date_count, 7, "Total Billed Amount", title_format)
        worksheet.write(row_date_count, 8, "Zip", title_format)
        worksheet.write(row_date_count, 9, "Area Group", title_format)
        worksheet.write(row_date_count, 10, "Repeat Customer", title_format)
        worksheet.write(row_date_count, 11, "Continue Today (last 20 days)", title_format)
        worksheet.write(row_date_count, 12, "Street", title_format)
        worksheet.write(row_date_count, 13, "Street1", title_format)
        worksheet.write(row_date_count, 14, "City", title_format)
        worksheet.write(row_date_count, 15, "State", title_format)
        # sheet.write(row_date_count, 16, "Initial Qty", title_style1_table_head_center)
        # sheet.write(row_date_count, 17, "Received Qty", title_style1_table_head_center)
        # sheet.write(row_date_count, 18, "F/Weight", title_style1_table_head_center)
        # sheet.write(row_date_count, 19, "By products weight", title_style1_table_head_center)



        row_date_count += 1
        count = 0
        values = []
        
        first_order_date = ''
        last_order_date = ''
        total_orders = ''
        fmt = '%Y-%m-%d %H:%M:%S'
        total_billed = 0
        zip = ''
        repeat_customer = ''
        last_twenty_days = 0
        street = ''
        street1 = ''
        city = ''
        state = ''

        for sale in self.env['sale.order'].search(
                [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)]):
           
            partner_obj = self.env['res.partner'].search([('name','=',sale.partner_id.name)])
            if partner_obj:
                for each in partner_obj:
                    total_orders = each.sale_order_count
                    if total_orders >1:
                        repeat_customer = 'Yes'
                    else:
                        repeat_customer = 'No'
                    total_billed = each.total_invoiced
                    zip = each.zip
                    street = each.street
                    street1 = each.street2
                    city = each.city
                    state = each.state_id.name
                    area = each.area
                    if each.sale_order_ids:
                        sale_obj = self.env['sale.order'].search([('partner_id','=',each.id)],order='id asc',limit=1)
                        first_order_date = datetime.strptime(str(sale_obj.date_order),'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')

                        sale_obj_last = self.env['sale.order'].search([('partner_id','=',each.id)],order='id desc',limit=1)

                        last_order_date = datetime.strptime(str(sale_obj_last.date_order),'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
                        current_date = (datetime.today()).strftime(fmt)
                        d1 = datetime.strptime(str(sale_obj_last.date_order), fmt)
                        d2 = datetime.strptime(current_date, fmt)
                        diff_days = (d2 - d1).days
                        if diff_days <= 20:
                            last_twenty_days = 'Yes'
                        else:
                            last_twenty_days = 'No'

                    name = each.name
                    ref = each.reference or ''
                    
                    data = {
                        'partner_name': name,
                        'reference': ref,
                        'source':each.customer_source_id.name or '',
                        'first_order_date':first_order_date,
                        'total_orders':total_orders,
                        'last_order_date': last_order_date,
                        'diff_days':diff_days,
                        'total_billed_amount':total_billed,
                        'zip_code':zip or '',
                        'area':area or '',
                        'repeat_customer': repeat_customer,
                        'last_twenty_days': last_twenty_days,
                        'street': street or '',
                        'street1':street1 or '',
                        'city': city or '',
                        'state': state or '',
                        
                    }
                    values.append(data)
                    print ("values",values)
        
        for val in values:
            count += 1
            # worksheet.write(row_date_count, 0, count, align_left)
            worksheet.write(row_date_count, 0, val['partner_name'], row_format)
            worksheet.write(row_date_count, 1, val['reference'], row_format)
            worksheet.write(row_date_count, 2, val['source'], row_format)
            worksheet.write(row_date_count, 3, val['first_order_date'], row_format)
            worksheet.write(row_date_count, 4, val['total_orders'], row_format)
            worksheet.write(row_date_count, 5, val['last_order_date'], row_format)
            worksheet.write(row_date_count, 6, val['diff_days'], row_format)
            worksheet.write(row_date_count, 7, val['total_billed_amount'], row_format)
            worksheet.write(row_date_count, 8, val['zip_code'], row_format)
            worksheet.write(row_date_count, 9, val['area'], row_format)
            worksheet.write(row_date_count, 10, val['repeat_customer'], row_format)
            worksheet.write(row_date_count, 11, val['last_twenty_days'], row_format)
            worksheet.write(row_date_count, 12, val['street'], row_format)
            worksheet.write(row_date_count, 13, val['street1'], row_format)
            worksheet.write(row_date_count, 14, val['city'], row_format)
            worksheet.write(row_date_count, 15, val['state'], row_format)    
            


            row_date_count += 1
        workbook.close()
        fp.seek(0)
        result = base64.b64encode(fp.read())
        
        report_id = self.env['sale.report.out'].sudo().create({'filedata': result, 'filename': 'sale report.xls'})
        print (report_id,"233333333333333")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=sale.report.out&field=filedata&id=%s&filename=%s.xls' % (report_id.id, 'sale report.xls'),
            'target': 'new',
            }
        # else:
        #     raise UserError(_('No records found'))


    # @api.multi
    def generate_excel_report(self):
        data = base64.encodestring(self.print_excel_report())
        report_name = 'Sale Report Excel.xls'
        report_id = self.env['sale.report.out'].sudo().create({'filedata': data, 'filename': 'sale report.xls'})
        print (report_id,"233333333333333")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=sale.report.out&field=filedata&id=%s&filename=%s.xls' % (report_id.id, report_name),
            'target': 'new',
            }


class SaleReportOut(models.TransientModel):
    
   _name = 'sale.report.out'
   
   filedata = fields.Binary('Download file', readonly=True)
   filename = fields.Char('Filename', size=64, readonly=True)
   
