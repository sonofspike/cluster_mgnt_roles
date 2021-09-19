# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url
import json
import request
import http.client
from requests.structures import CaseInsensitiveDict
from ansible.module_utils.six import PY2
from ansible.module_utils import HTTPError, URLError
from ansible.module_utils import urlencode, quote
from ansible.module_utils.urls import Request, basic_auth_header

from .errors import AssistedInstallerError, AuthError, UnexpectedAPIResponse


DEFAULT_HEADERS = dict(Accept="application/json")


class Response:
    def __init__(self, status, data, headers=None):
        self.status = status
        self.data = data
        # [('h1', 'v1'), ('H2', 'V2')] -> {'h1': 'v1', 'h2': 'V2'}
        self.headers = dict((k.lower(), v) for k, v in dict(headers).items()) if headers else {}

        self._json = None

    @property
    def json(self):
        if self._json is None:
            try:
                self._json = json.loads(self.data)
            except ValueError:
                raise AssistedInstallerError(
                    "Received invalid JSON response: {0}".format(self.data)
                )
        return self._json


class Client:
    def __init__(
        self, host, username=None, password=None, grant_type=None,
        refresh_token=None, client_id=None, client_secret=None, timeout=None
    ):

        if not (host or "").startswith(('https://', 'http://')):
            raise AssistedInstallerError("Invalid instance host value: '{0}'. "
                                  "Value must start with 'https://' or 'http://'".format(host))

        self.host = host
        self.username = username

        self.password = password
        self.grant_type = grant_type

        self.client_id = client_id
        self.client_secret = client_secret

        self.refresh_token = refresh_token
        self.timeout = timeout

        self._auth_header = None
        self._client = Request()

    def get(self, path, query=None):
        resp = self.request("GET", path, query=query)
        if resp.status in (200):
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def post(self, path, data, query=None):
        resp = self.request("POST", path, data=data, query=query)
        if resp.status == 201:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def patch(self, path, data, query=None):
        resp = self.request("PATCH", path, data=data, query=query)
        if resp.status == 200:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def put(self, path, data, query=None):
        resp = self.request("PUT", path, data=data, query=query)
        if resp.status == 200:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def delete(self, path, query=None):
        resp = self.request("DELETE", path, query=query)
        if resp.status != 204:
            raise UnexpectedAPIResponse(resp.status, resp.data)

    def create_cluster(module):
        path = module.params["api_base_url"]
        request = self.post(path, data=data, query=query)

def main():
    fields = {
        "api_base_url": {"type": "str"},
        "validate_certs": {"type": "bool", "default": "true"},
        "api_token": {"type": "str"},
          }
    required_together = [["api_base_url", "api_token"]]

    #module parameter
    module = AnsibleModule(
        argument_spec=fields,
        required_together=required_together,
        supports_check_mode=True
    )
    (changed, result, status_code) = create_cluster(module)
    module.exit_json(changed=changed, ansible_facts=result, status_code=status_code)
#class constructor
if __name__ == "__main__":
    main()
