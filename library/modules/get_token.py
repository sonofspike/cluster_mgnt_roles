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

def get_token(module):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    result = dict(
        changed=False,
        original_message='',
        message='',
        my_useful_info={},
    )

    api_token = module.params["api_token"]
    data = {"grant_type":"refresh_token", "client_id": "cloud-services", "refresh_token": api_token}
    url = module.params["api_base_url"]
    response = requests.post(url, headers=headers, data=data)
    

    #response = requests.request(method="POST", url=url, headers=headers, data=payload)
        #Performs a POST on the specified url to get the token
    if response.status_code == 200 or 201:
        try:    
            print(response.status_code)
            result['message'] = response.content
            access_token = response.json()['access_token']
            rec = { "access_token": access_token }
            token = json.dumps(data, separators=(",", ":"))
       
            exp = response.json()
            expires_in = exp.get("expires_in")

            ansible_facts_dict = {
            "changed" : True,
            "rc" : 5,
            "ansible_facts" : {
            "access_token" : access_token
            }
            }
            module.exit_json(changed=True,msg=[access_token,expires_in])

        except Exception as e:
                module.fail_json(
                    msg="Error obtaining token\n%s" % (to_text(e)),
                    headers=headers,
                    status_code=-1,
                )

        else:
            module.fail_json(
                    msg="error",
                    headers=headers,
                    status_code=-1,
                )
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
    (changed, result, status_code) = get_token(module)
    module.exit_json(changed=changed, ansible_facts=result, status_code=status_code)
#class constructor
if __name__ == "__main__":
    main()
