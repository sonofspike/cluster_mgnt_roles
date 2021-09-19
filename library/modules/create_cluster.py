import urllib
from urllib import error as error
import urllib.request
import ssl
import json
from string import Template
import types
from ansible.module_utils.basic import AnsibleModule
#from module_utils.init.http_request import http_post, http_request
from ansible.module_utils._text import to_text
from ansible.module_utils.urls import open_url
from module_utils import http_post
import requests
import http.client
from requests.structures import CaseInsensitiveDict


def __create_cluster(module):
        result = dict(
        changed=False,
        original_message='',
        message='',
        my_useful_info={},
    )
        data = { "name": module.params["name"],
             "openshift_version": module.params["openshift_version"], 
             "base_dns_domain": module.params["base_dns_domain"],
             "cluster_network_cidr": module.params["cluster_network_cidr"],
             "cluster_network_host_prefix": 23,
             "high_availability_mode": None,
             "service_network_cidr": module.params["service_network_cidr"],
             "pull_secret": module.params["pull_secret"],
             "ssh_public_key": module.params["ssh_public_key"],
             "vip_dhcp_allocation": module.params["vip_dhcp_allocation"],
             "http_proxy": module.params["http_proxy"],
             "https_proxy": module.params["https_proxy"],
             "no_proxy": module.params["no_proxy"],
             "additional_ntp_source":  module.params["ntp_source"]
            }
        base_url = module.params.get("url_assisted_installer")
        url = base_url + "/clusters"
        header = { "Authorization": 'Bearer '+module.params.get("access_token"),
        "Content-Type": 'application/json'}
        headers = CaseInsensitiveDict(header)
        path = "/clusters"
        access_token = module.params.get("access_token")
        request = http_post(url, access_token, data=json.dumps(data))
        if request == 200 or 201:
            try:    
                print(request)
                token = json.dumps(data, separators=(",", ":"))

                module.exit_json(msg=request)

            except Exception as e:
                    module.fail_json(
                        msg="Error",
                        headers=headers
                    )
def main():

    fields = { "name": {"type": "str"},
             "url_assisted_installer": {"type": "str"},
             "openshift_version": {"type": "str"}, 
             "access_token": {"type": "str"},
             "base_dns_domain": {"type": "str"},
             "cluster_network_host_prefix": {"type": "int"},
             "cluster_network_cidr":{"type": "str"},
             "high_availability_mode":{"type": "str"},
             "service_network_cidr": {"type": "str"},
             "pull_secret": {"type": "str"},
             "ssh_public_key": {"type": "str"},
             "vip_dhcp_allocation": {"type": "bool"},
             "http_proxy": {"type": "str"},
             "https_proxy": {"type": "str"},
             "no_proxy": {"type": "str"},
             "ntp_source":  {"type": "str"}
            }


    required_together = [["url_assisted_installer", "access_token"]]

    #module parameter
    module = AnsibleModule(
        argument_spec=fields,
        required_together=required_together,
        supports_check_mode=True
    )
    (changed, result, status_code) = __create_cluster(module)
    module.exit_json(changed=changed, ansible_facts=result, status_code=status_code)
if __name__ == '__main__':
    from ansible.module_utils.basic import * 

    main()

