# -*- coding: utf-8 -*-

import requests
import logging
from ast import literal_eval
from .auth_token import get_authentication_token
from odoo.exceptions import ValidationError

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class AppCategory(models.Model):
    _name = "app.category"
    _description = "App Category"

    name = fields.Char("Category Name", required=True)
    image = fields.Image("Image")
    image_url = fields.Char("Image Url")
    child_id = fields.One2many('app.subcategory', 'category_id', 'Sub Categories')

    is_update = fields.Boolean("Is Update ?")

    def sync_data_to_mobile_app(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'Content-type': 'application/json', 'Accept': 'text/plain'}
        arguments = {
            'category_name': self.name,
            'category_imgurl': self.image_url,
        }
        if self.is_update:
            url = base_url + '/category/' + str(self.id)
            r = requests.put(url, json=arguments, headers=headers, timeout=30)
            result = literal_eval(r.text)
            if 'errors' in result:
                raise ValidationError("not synced bcoz of %s" % (result['errors']))
        else:
            arguments.update({'category_id_ODOO': self.id})
            url = base_url + '/category/'
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
        _logger.info("Category Synced to mobile app %s" % result)

    def unlink(self):
        if self.is_update:
            base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
            jwt_token = get_authentication_token(base_url=base_url)
            headers = {'x-auth-token': jwt_token,
                       'Content-type': 'application/json', 'Accept': 'text/plain'}
            arguments = {}
            url = base_url + '/category/' + str(self.id)
            r = requests.delete(url, json=arguments, headers=headers, timeout=30)
            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': arguments,
                'response': result
            })
            _logger.info("Category deleted from mobile app %s" % result)
        return super().unlink()


class AppSubCategory(models.Model):
    _name = "app.subcategory"
    _description = "App Sub Category"

    name = fields.Char("Category Name", required=True)
    category_id = fields.Many2one('app.category', string="Parent Category", required=True)
    # image = fields.Image("Image")

    is_update = fields.Boolean("Is Update ?")

    def sync_data_to_mobile_app(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
        jwt_token = get_authentication_token(base_url=base_url)
        headers = {'x-auth-token': jwt_token,
                   'Content-type': 'application/json', 'Accept': 'text/plain'}
        arguments = {
            'sub_category_name': self.name,
            'parent_id': self.category_id.id,
        }
        if self.is_update:
            url = base_url + '/subcategory/' + str(self.id)
            r = requests.put(url, json=arguments, headers=headers, timeout=30)
            result = literal_eval(r.text)
            if 'errors' in result:
                raise ValidationError("not synced bcoz of %s" % (result['errors']))
        else:
            arguments.update({'sub_category_id_ODDO': self.id})
            url = base_url + '/subcategory/'
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
        _logger.info("Category Synced to mobile app %s" % result)

    def unlink(self):
        if self.is_update:
            base_url = self.env['ir.config_parameter'].sudo().get_param('truegood.api_url')
            jwt_token = get_authentication_token(base_url=base_url)
            headers = {'x-auth-token': jwt_token,
                       'Content-type': 'application/json', 'Accept': 'text/plain'}
            arguments = {}
            url = base_url + '/subcategory/' + str(self.id)
            r = requests.delete(url, json=arguments, headers=headers, timeout=30)
            result = literal_eval(r.text)
            api_tracker = self.env['oi.api.tracker'].sudo().create({
                'name': url,
                'request_body': arguments,
                'response': result
            })
            _logger.info("Sub Category deleted from mobile app %s" % result)
        return super().unlink()
