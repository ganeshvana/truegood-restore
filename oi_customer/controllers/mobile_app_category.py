# -*- coding: utf-8 -*-

import json
from .token import has_valid_token
from odoo.http import Controller, Response, request, route


class CategoryApi(Controller):

    @route('/getAllCategory', type="json", auth='public', methods=["GET"], csrf=False)
    @has_valid_token
    def get_allcategory(self):
        categories = request.env['app.category'].sudo().search([])
        if categories:
            category_list = []
            for category in categories:
                details = {
                    'category_id': category.id,
                    'category_name': category.name,
                    'category_imgUrl': category.image_url
                }
                category_list.append(details)

            return {"session_valid": True,
                    "response_code": 200,
                    "status": "success",
                    "message_code": "CATEGORY",
                    "message": "Category List.",
                    "payload": category_list}
        else:
            return {"message": "There are no categories found !"}

    @route('/subcategory', type="json", auth='public', methods=["GET"], csrf=False)
    @has_valid_token
    def get_subcategory_list(self):
        data = request.jsonrequest
        if data:
            category_id = int(data.get('category_id'))
            if category_id:
                categ_obj = request.env['app.category'].sudo().browse(category_id)
                sub_categories = categ_obj.child_id
                if sub_categories:
                    categ_list = []
                    for category in sub_categories:
                        categ_list.append({
                            'subcategory_id': category.id,
                            'subcategory_name': category.name
                        })

                    return {"session_valid": True,
                            "response_code": 200,
                            "status": "success",
                            "message_code": "CATEGORY",
                            "message": "SubCategory List.",
                            "payload": categ_list}
                else:
                    return {"message": "There are no subcategory for this category !"}
            else:
                return {"message": "There are no category in this id !"}
