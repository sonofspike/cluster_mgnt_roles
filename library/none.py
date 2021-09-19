import urllib
import ssl
import json
from string import Template
import types
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
import requests
from requests import Request, Session
from requests.structures import CaseInsensitiveDict

## Constants:
API_BASE = "/api/v1"


    
########################### Helper methods/Primative ###################################
#
# This section contains helper methods for Assisted Installer
#
################################################################################


def http_get(path, module):
    return http_request("GET", path, module, "")

def http_post(module, data):
        result = dict(
        changed=False,
        original_message='',
        message='',
        my_useful_info={},
    )
        path = "/clusters"
  
        return http_request("POST", path, module, data)

def http_put(path, module, data):
    return http_request("PUT", path, module, data)

def http_delete(path, module):
    return http_request("DELETE", path, module, "")

def http_request(method, path, module, data):
    try:
        url = module.params.get("url_assisted_installer")+path
        #opener = urllib2.build_opener(urllib2.HTTPHandler)

        headers = { "Authorization": 'Bearer '+module.params.get("access_token"),
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
            if resp.status_code == 200 or 201:
                try:    
                    print(resp.status_code)

                    module.exit_json(msg=resp.text)

                except Exception as e:
                        module.fail_json(
                            msg="Error",
                            headers=headers,
                            status_code=resp.status_code
                    )
        elif method == "PUT":
            s = Session()
            req = Request('PUT', url, data=data, headers=header)
            prepped = req.prepare()
            resp = s.send(prepped)
            print(resp.status_code)
            
      
    except urllib.error.HTTPError as sc:
        if sc.code == 401:
            msg = "authenication error (401):"
            module.fail_json(msg=msg)

        elif sc.code == 409:
            msg = "Can't update resource:"
            module.fail_json(msg=msg)
        elif sc.code == 422:
            msg = " Unprocessable Enitiy (422):"
            module.fail_json(msg=msg)
        elif sc.code == 400:
            msg = "Bad Request (400):"
            module.fail_json(msg=msg)
        else:
            raise sc


    except urllib.error.URLError as ue:
        module.fail_json(msg="Assisted Installer is unreachable. Check connection and master_url setting.")

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
    (changed, result, status_code) = http_post(module)
    module.exit_json(changed=changed, ansible_facts=result, status_code=status_code)
if __name__ == '__main__':
    main()


