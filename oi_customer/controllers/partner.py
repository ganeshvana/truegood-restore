# -*- coding: utf-8 -*-

from .token import has_valid_token
from odoo.http import Controller, Response, request, route


class CustomerApi(Controller):

    @route('/getCustomerById', type="json", auth='public', methods=["GET"], csrf=False)
    @has_valid_token
    def get_category(self):
        data = request.jsonrequest
        api_tracker = request.env['oi.api.tracker'].sudo().create({
            'name': '/getCustomerById',
            'request_body': data,
            'response': ''
        })
        if data:
            customer_id = data.get('customer_id')
            customer = request.env["res.partner"].sudo().search([('mobile_ref', '=', customer_id)])
            if customer:
                customer_details = {
                    "mobile_ref": customer_id,
                    "name": customer.name,
                    "mobile": customer.mobile,
                    "ref": customer.mobile,
                    "email": customer.email,
                    "street": customer.street,
                    "city": customer.city,
                    "state": customer.state_id.code
                }
                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "CUSTOMER",
                        "message": "Customer Details.",
                        "payload": customer_details}
            else:
                return {"message": "Customer With this ID does not exist !"}

    @route('/customer/create', type="json", auth='public', methods=["POST"], csrf=False)
    @has_valid_token
    def create_customer(self):
        data = request.jsonrequest
        api_tracker = request.env['oi.api.tracker'].sudo().create({
            'name': '/customer/create',
            'request_body': data,
            'response': ''
        })
        if data:
            customer_id = data.get('customer_id')
            customer = request.env["res.partner"].sudo().search([('mobile_ref', '=', customer_id)])
            if customer:
                return {"message": "Customer With same ID already exist !"}
            else:
                customer_data_list = data.get('data')
                for cd in customer_data_list:
                    contact = {
                        "mobile_ref": customer_id,
                        "company_type": "person",
                        "name": cd.get("full_name"),
                        "mobile": cd.get("phone_number"),
                        "ref": cd.get("phone_number"),
                        "email": cd.get("email"),
                        "street": cd.get("street"),
                        "city": cd.get("city"),
                    }
                    state = request.env['res.country.state'].sudo().search(
                        [('code', '=', cd.get('state_code')), ('country_id.code', '=', 'IN')])
                    if state:
                        contact.update({"state_id": state.id})
                    customer.sudo().create(contact)
                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "CUSTOMER_CREATED",
                        "message": "Customer created successfully.",
                        "payload": []}

    @route('/customer/update', type="json", auth='public', methods=["PUT"], csrf=False)
    @has_valid_token
    def update_customer(self):
        data = request.jsonrequest
        api_tracker = request.env['oi.api.tracker'].sudo().create({
            'name': '/customer/update',
            'request_body': data,
            'response': ''
        })
        if data:
            customer_id = data.get('customer_id')
            customer = request.env["res.partner"].sudo().search([('mobile_ref', '=', customer_id)])
            customer_data_list = data.get('data')
            if customer:
                for cd in customer_data_list:
                    contact = {
                        "company_type": "person",
                        "name": cd.get("full_name"),
                        "mobile": cd.get("phone_number"),
                        "ref": cd.get("phone_number"),
                        "email": cd.get("email"),
                        "street": cd.get("street"),
                        "city": cd.get("city"),
                    }
                    state = request.env['res.country.state'].sudo().search(
                        [('code', '=', cd.get('state_code')), ('country_id.code', '=', 'IN')])
                    if state:
                        contact.update({"state_id": state.id})
                    customer.sudo().write(contact)

                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "CUSTOMER_UPDATED",
                        "message": "Customer information updated successfully.",
                        "payload": []}
            return {"message": "Customer not found"}

    @route('/customer/addAddress', type="json", auth='public', methods=["POST"], csrf=False)
    @has_valid_token
    def add_customer_address(self):
        data = request.jsonrequest
        api_tracker = request.env['oi.api.tracker'].sudo().create({
            'name': '/customer/addAddress',
            'request_body': data,
            'response': ''
        })
        if data:
            customer_id = data.get('customer_id')
            customer = request.env["res.partner"].sudo().search([('mobile_ref', '=', customer_id)])
            customer_data_list = data.get('address')
            if customer:
                for cd in customer_data_list:
                    address = {
                        "mobile_ref": cd.get('address_id'),
                        "delivery_address_type": cd.get("delivery_address_type"),
                        "type": cd.get("type"),
                        "parent_id": customer.id,
                        "company_type": "person",
                        "name": cd.get("full_name"),
                        "mobile": cd.get("phone_number"),
                        "ref": cd.get("phone_number"),
                        "email": cd.get("email"),
                        "street": cd.get("street"),
                        "street2": cd.get("street2"),
                        "zip": cd.get("zip"),
                        "city": cd.get("city"),
                    }
                    state = request.env['res.country.state'].sudo().search(
                        [('code', '=', cd.get('state_code')), ('country_id.code', '=', 'IN')])
                    if state:
                        address.update({"state_id": state.id})
                    customer.sudo().create(address)

                return {"session_valid": True,
                        "response_code": 200,
                        "status": "success",
                        "message_code": "CUSTOMER",
                        "message": "Customer address added successfully.",
                        "payload": []}
            return {"message": "Customer not found"}
