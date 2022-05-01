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

class OrdersaleReport(models.Model):
    _name = 'order.sale.report'

   
    # partner_id = fields.Many2one('res.partner', string="Customer")
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)



    def get_datas(self):
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        # workbook = xlwt.Workbook()
        title_format = workbook.add_format(
            {'font_name': 'TimesNew Roman', 'font_size': 11, 'align': 'center','bold': 1,'color':'red'})
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
        worksheet = workbook.add_worksheet('Sale Order Report')

        worksheet.merge_range(0,0,0,4,'True Good Essentials',title_format)
        worksheet.merge_range(2,2,5,7,'Sale Order Report',title_format)
        worksheet.write(row_date_count, 0, "W SL", title_format)
        worksheet.write(row_date_count, 1, "Sales Order No.", title_format)
        worksheet.write(row_date_count, 2, "Invoice No.", title_format)
        worksheet.write(row_date_count, 3, "Planned Delivery Date", title_format)
        worksheet.write(row_date_count, 4, "Customer Name", title_format)
        worksheet.write(row_date_count, 5, "Phone", title_format)
        worksheet.write(row_date_count, 6, "Address", title_format)
        worksheet.write(row_date_count, 7, "Zip", title_format)
        worksheet.write(row_date_count, 8, "Area Group", title_format)
        worksheet.write(row_date_count, 9, "Payable Amount", title_format)
        worksheet.write(row_date_count, 10, "Date of Order", title_format)
        worksheet.write(row_date_count, 11, "Time of Order", title_format)
        worksheet.write(row_date_count, 12, "Sale Order made by", title_format)
        worksheet.write(row_date_count, 13, "Delivery by", title_format)
        worksheet.write(row_date_count, 14, "Delivery date", title_format)
        

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

        for ids,sale in enumerate (self.env['sale.order'].search(
                [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)])):
           
            invoice_obj = self.env['account.move'].search([('invoice_origin','=',sale.name)])
            first_order_date = datetime.strptime(str(sale.date_order),'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
            times = datetime.strptime(str(sale.date_order),'%Y-%m-%d %H:%M:%S').strftime('%H:%M')
            commitmentdate = datetime.strptime(str(sale.commitment_date),'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
            Deliverydates = sale.actual_delivery_date
            if Deliverydates:
                Deliverydate = datetime.strptime(str(sale.actual_delivery_date),'%Y-%m-%d').strftime('%d/%m/%Y')
            else:
                Deliverydate=''
            li = []
            street = sale.partner_id.street
            city = sale.partner_id.city
            state = sale.partner_id.state_id.name
            zips = sale.partner_id.zip

            li.append(str(street));li.append(str(city));li.append(str(" "+str(zips)));li.append(str(" "+str(state)));
            address = ''.join(li)
            
            
            for data_invoice in invoice_obj:
                
                data = {
                    'wsl':ids,
                    'Sales_OrderNo': sale.name,
                    'Invoice':data_invoice.name,
                    'Planned_Delivery_Date': commitmentdate,
                    'Customer_Name': sale.partner_id.name,
                    'Phone':sale.partner_id.phone,
                    'zip':sale.partner_id.zip,
                    'Date_of_Order':commitmentdate,
                    'timeorder':times,
                    'Address':address,
                    'Amount':data_invoice.amount_total,
                    'made':sale.user_id.name,
                    'Deliveryby':'',
                    'Deliverydate':Deliverydate,
                    'area':sale.area or '',
                }
                values.append(data)
                
        
        for val in values:
            count += 1
            # worksheet.write(row_date_count, 0, count, align_left)
            worksheet.write(row_date_count, 0, val['wsl'], row_format)
            worksheet.write(row_date_count, 1, val['Sales_OrderNo'], row_format)
            worksheet.write(row_date_count, 2, val['Invoice'], row_format)
            worksheet.write(row_date_count, 3, val['Planned_Delivery_Date'], row_format)
            worksheet.write(row_date_count, 4, val['Customer_Name'], row_format)
            worksheet.write(row_date_count, 5, val['Phone'], row_format)
            worksheet.write(row_date_count, 6, val['Address'], row_format)
            worksheet.write(row_date_count, 7, val['zip'], row_format)
            worksheet.write(row_date_count, 8, val['area'], row_format)
            worksheet.write(row_date_count, 9, val['Amount'], row_format)
            worksheet.write(row_date_count, 10, val['Date_of_Order'], row_format)
            worksheet.write(row_date_count, 11, val['timeorder'], row_format)
            worksheet.write(row_date_count, 12, val['made'], row_format)
            worksheet.write(row_date_count, 13, val['Deliveryby'], row_format)
            worksheet.write(row_date_count, 14, val['Deliverydate'], row_format)
            
            
            


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


class SaleReportOuts(models.TransientModel):
    
   _name = 'sale.report.out'
   
   filedata = fields.Binary('Download file', readonly=True)
   filename = fields.Char('Filename', size=64, readonly=True)
   
