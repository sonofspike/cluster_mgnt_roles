#!/usr/bin/python
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "certified",
}

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url
import json
import requests
import http.client
from requests.structures import CaseInsensitiveDict

def refresh_token(module):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    result = dict(
        changed=False,
        original_message='',
        message='',
        my_useful_info={},
    )

    api_token = open("api_token.txt", "r")

    data = {"grant_type":"refresh_token", "client_id": "cloud-services", "refresh_token": api_token}
    url = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
    response = requests.post(url, headers=headers, data=data)
    

    #response = requests.request(method="POST", url=url, headers=headers, data=payload)
        #Performs a POST on the specified url to get the token
    if response.status_code == 200 or 201:
        try:    
            print(response.status_code)
            result['message'] = response.content
            token = response.json()['access_token']
            print(token)
            result['message'] = token
            token = json.dumps(response.content, separators=(",", ":"))
            module.exit_json(msg=token)

        except Exception as e:
                module.fail_json(
                    msg="Error obtaining token\n%s" % (to_text(e)),
                    headers=headers,
                    status_code=-1,
                )


def main():
    fields = {
        "api_base_url": {"type": "str"},
        "validate_certs": {"type": "bool", "default": "true"},
        "api_token": {"type": "str"},
          }

    #module parameter
    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=True
    )
    (changed, result, status_code) = refresh_token(module)
    module.exit_json(changed=changed, ansible_facts=result, status_code=status_code)
#class constructor
if __name__ == "__main__":
    main()
