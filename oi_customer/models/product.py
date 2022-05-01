# -*- coding: utf-8 -*-

import requests
import logging
from ast import literal_eval
from .auth_token import get_authentication_token

from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_url = fields.Char("Image Url")
    app_category = fields.Many2one('app.category', string="App Category")
    app_subcategory = fields.Many2one('app.subcategory', string="App Sub Category")
    keyword_search = fields.Many2many('product.keyword', 'product_tag_rel', 'product_id', 'keyword_id',
                                      string='Search Keywords', help="Search the products using following keywords in mobile app")
    is_offer_product = fields.Boolean("Is Offer Product ?")
    is_bestseller = fields.Boolean("Best Seller")
    is_recommended = fields.Boolean("Recommended")
    offer_price = fields.Float(
        'Offer Price',
        digits='Product Price',
        help="Offer Price at which the product is sold to customers.")

    is_update = fields.Boolean("Is Update ?")

    def delete_product_from_mobile_app(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'Content-type': 'application/json', 'Accept': 'text/plain'}
        arguments = {}
        url = base_url + '/product/' + str(self.product_variant_id.id)
        r = requests.delete(url, json=arguments, headers=headers, timeout=30)
        result = literal_eval(r.text)
        api_tracker = self.env['oi.api.tracker'].sudo().create({
            'name': url,
            'request_body': arguments,
            'response': result
        })
        _logger.info("Product deleted from mobile app %s" % result)

    def sync_data_to_mobile_app(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'Content-type': 'application/json', 'Accept': 'text/plain'}

        name = self.name.split("-", 1)
        arguments = {
            'product_name': name[0] if name[0] else self.name,
            'last_name': name[1] if name[1] else self.name,
            'product_imgurl': self.image_url if self.image_url else '',
            'product_price': self.lst_price if self.lst_price else '',
            'is_recommended': self.is_recommended,
            'is_bestseller': self.is_bestseller,
            'isOffer': self.is_offer_product,
            'offer_price': self.offer_price if self.is_offer_product else 0,
            'product_weight': self.weight if self.weight else '',
            'product_discount': '',
            'item_stock': self.qty_available,
            'product_description': self.description_sale if self.description_sale else '',
            'product_category': self.app_category.id if self.app_category.id else '',
            'product_subcategory': self.app_subcategory.id if self.app_subcategory.id else '',
            'product_uom': name[1] if name[1] else self.uom_id.name,
            'product_taxes': [tax.amount for tax in self.taxes_id] if self.taxes_id else '',
            'search_keywords': [keyword.name for keyword in self.keyword_search] if self.keyword_search else ''
        }
        if self.is_update:
            url = base_url + '/product/' + str(self.product_variant_id.id)
            r = requests.put(url, json=arguments, headers=headers, timeout=30)
            result = literal_eval(r.text)
            if 'errors' in result:
                raise ValidationError("not synced bcoz of %s" % (result['errors']))
        else:
            arguments.update({'product_id_ODDO': self.product_variant_id.id})
            url = base_url + '/product/'
            r = requests.post(url, json=arguments, headers=headers, timeout=30)
            result = literal_eval(r.text)
            if 'errors' in result:
                raise ValidationError("not synced bcoz of %s" % (result['errors']))
            self.is_update = True
        api_tracker = self.env['oi.api.tracker'].sudo().create({
            'name': url,
            'request_body': arguments,
            'response': result
        })
        _logger.info("Product Synced to mobile app %s" % result)

    def unlink(self):
        if self.is_update:
            base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
            jwt_token = get_authentication_token(base_url=base_url)
            headers = {'x-auth-token': jwt_token,
                       'Content-type': 'application/json', 'Accept': 'text/plain'}
            arguments = {}
            url = base_url + '/product/' + str(self.product_variant_id.id)
            r = requests.delete(url, json=arguments, headers=headers, timeout=30)
            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': arguments,
                'response': result
            })
            _logger.info("Product deleted from mobile app %s" % result)
        return super().unlink()


class ProductKeywords(models.Model):
    _name = 'product.keyword'
    _description = "Search Keywords"

    name = fields.Char("Search Keyword")
