# -*- coding: utf-8 -*-

import requests
import json
from ast import literal_eval


def get_authentication_token(base_url):
    auth_url = base_url + '/customer/loginSocial'
    headers = {'content-type': 'application/json'}
    arguments = {"email": "truegood@gmail.com",
                 "name": "truegood"}
    r = requests.post(auth_url, data=json.dumps(arguments), headers=headers, timeout=30)
    result = literal_eval(r.text)
    jwt_token = result.get('token')
    return jwt_token
