from locale import Error
import urllib
import ssl
import json
from string import Template
import types
import requests
from requests import Request, Session
from requests.structures import CaseInsensitiveDict
from ansible.module_utils.basic import *
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# Important contants
from ansible import constants as C
# Common error handlers
from ansible.errors import AnsibleError
# Use Ansible's builtin boolean type if needed
from ansible.module_utils.parsing.convert_bool import boolean
# ADT base class for our Ansible Action Plugin
from ansible.plugins.action import ActionBase
## Constants:
API_BASE = "/api/v1"


    
########################### Helper methods/Primative ###################################
#exi
# This section contains helper methods for Assisted Installer
#
################################################################################

class http_request():
    def __init__(self, request):
        self.request = self.http_post
    def http_get(path, module):
        return http_request("GET", path, module, "")

    def http_post(url, access_token, status_code, data):
        return http_request("POST", url, access_token, status_code, data)

    def http_put(path, url, access_token, data):
        return http_request("PUT", path,  url, access_token, data)

    def http_delete(path, module):
        return http_request("DELETE", path, module, "")

    def http_request(method,url, access_token, status_code, data):
        try:
            #opener = urllib2.build_opener(urllib2.HTTPHandler)

            headers = { "Authorization": 'Bearer ' +access_token,
            "Content-Type": 'application/json'}        #GET
            header = CaseInsensitiveDict(headers)


            if method == "DELETE":
                s = Session()

                req = Request('DELETE', url, data=data, headers=header)
                prepped = req.prepare()
                resp = s.send(prepped)
                print(resp.status_code)

            elif method == "POST":
                s = Session()

                req = Request('POST', url, data=json.dumps(data), headers=header)
                prepped = req.prepare()
                resp = s.send(prepped)
                print(resp.status_code)
                status_code = resp.status_code

                if status_code == 200 or 201:
                    try:    
                        print(status_code)
                        return status_code

                    except Exception as e:
                            raise e
            elif method == "PUT":
                s = Session()
                req = Request('PUT', url, data=data, headers=header)
                prepped = req.prepare()
                resp = s.send(prepped)
                print(resp.status_code)
                
        
        except urllib.error.HTTPError as sc:
            if sc.code == 401:
                msg = "authenication error (401):"
                return status_code

            elif sc.code == 409:
                msg = "Can't update resource:"
                return status_code

            elif sc.code == 422:
                msg = " Unprocessable Enitiy (422):"
                return status_code

            elif sc.code == 400:
                msg = "Bad Request (400):"
                return status_code

            else:
                raise sc


        except urllib.error.URLError as ue:
            raise ue
    def main():

        fields = None

    if __name__ == '__main__':
        main()

