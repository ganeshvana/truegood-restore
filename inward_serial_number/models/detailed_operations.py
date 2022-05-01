# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import pdb

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    def create_serial_number(self):
        view = self.env.ref('stock.view_stock_move_operations')
        count = 0
        serial_no = ''
        for rec in self:
            if not rec.picking_id.backorder_id:
                if rec.move_line_nosuggest_ids:
                    for line in rec.move_line_nosuggest_ids:
                        count += 1
                        serial_no = str(rec.picking_id.origin) + str(rec.product_id.name) + str(line.qty_done) + '-' + str(count)
                        line.lot_name = serial_no
                        line.lot_seq = count
                    count = 0
            if rec.picking_id.backorder_id:
                if rec.picking_id.backorder_id.move_ids_without_package:
                    for move in rec.picking_id.backorder_id.move_ids_without_package:
                        if move.move_line_nosuggest_ids:
                            if move.product_id == rec.product_id:
                                last_line = self.env['stock.move.line'].search([('move_id', '=', move.id)], order='lot_seq desc', limit=1)
                                if last_line:
                                    count = last_line.lot_seq
                                    for line in rec.move_line_nosuggest_ids:    
                                        count += 1                                    
                                        serial_no = str(rec.picking_id.origin) + str(rec.product_id.name) + str(line.qty_done) + '-' + str(count)
                                        line.lot_name = serial_no
                                        line.lot_seq = count
                                    count = 0
        return {
            'name': _('Detailed Operations'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.move',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'nodestroy': True,
            'context': dict(
                self.env.context,
                move_line_nosuggest_ids = self.move_line_nosuggest_ids.ids,
                reserved_availability = self.reserved_availability
                )
            
        }
        
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    lot_seq = fields.Integer("Lot Seq")