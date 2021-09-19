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
class ActionModule(ActionBase):
    # Some plugins may use class constants to control behavior.
    # In the case of TRANSFERS_FILES it is used by ActionBase to determine at which point in execution
    # temporary directories need to be available if your Action Plugin is using modules to
    # transfer files.
    TRANSFERS_FILES = False

    # The run method is the main Action Plugin driver. All work is done from within this method.
    #
    # tmp: Temporary directory. Sometimes an action plugin sets up
    #      a temporary directory and then calls another module. This parameter
    #      allows us to reuse the same directory for both.
    # task_vars: The variables (host vars, group vars, config vars, etc) associated with this task.
    #            Note that while this will contain Ansible facts from the host, they should be used
    #            with caution as a user running Ansible can disable their collection. If you want
    #            make sure that your Action Plugin always has access to the ones it needs, you may
    #            want to consider running the setup module directly in the run the method and getting
    #            the Ansible facts that way.
    #            The stragety plugin which manages running tasks on instances uses an ansible.vars.manager
    #            VariableManager instance to retrieve this context specific dict of variables.
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

    def run(self, tmp=None, task_vars=None):
        # Initialize our parent. The returned result is normally an empty dict unless you are inheriting
        # from another subclass of ActionBase that does other tasks in its run instance method. Otherwise,
        # all the run will do is a validation.
        #
        # For a list of common properties included in a result, see ansible/utils/module_docs_fragments/return_common.py
        result = super(ActionModule, self).run(tmp, task_vars)
        
        # Initialize result object with some of the return_common values:
        result.update(
            dict(
                changed=False,
                failed=False,
                msg='',
                skipped=False
            )
        )

        # Define support for check mode and async
        self._supports_check_mode = True
        self._supports_async = False

        # Execute another Ansible module
        setup_module_args=dict(
            gather_subset='all',
            gather_timeout=10
        )

        # Run the setup module to collect facts
        #
        # delete_remote_tmp: Boolean that determines whether the remote tmp directory and files are deleted.
        # module_name: The name of the Ansible module to run.
        # module_args: A dict of arguments to provide to the Ansible module.
        # persist_files: Boolean that determins whether or not to keep temporary files.
        # task_vars: The task variables for the current play context.
        # tmp: The path to the temporary directory.
        # wrap_async: Boolean that controls whether or not the task is run asyncronously.
        setup_result = self._execute_module(
            delete_remote_tmp=True,
            module_name='setup',
            module_args=setup_module_args,
            persist_files=False,
            task_vars=task_vars,
            tmp=tmp,
            wrap_async=self._task
        )

        if setup_result['ansible_facts']['ansible_system'] != 'Linux':
            result['failed'] = True

        return result

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

