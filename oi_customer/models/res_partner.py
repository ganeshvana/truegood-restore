# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Partner(models.Model):

    _inherit = 'res.partner'

    mobile_ref = fields.Char("Mobile App Reference")

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('mobile', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
