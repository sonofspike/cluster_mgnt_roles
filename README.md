# OpenShift 4 Management Cluster Seed Playbook (Online API Assisted Installer)

> :heavy_exclamation_mark: *Red Hat does not provide commercial support for the content of this repo*

```bash
##############################################################################
DISCLAIMER: THE CONTENT OF THIS REPO IS PROVIDED "AS-IS"

THE CONTENT IS PROVIDED AS REFERENCE WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
##############################################################################
```

This playbook is responsible for automating the creation of an OpenShift Container Platform (4.6) cluster using the Developer Preview version of the OpenShift Assisted Installer. Virtual and bare metal machines have been tested in a regular deployment (where systems can reach `registry.redhat.io` and `redhat.com` directly without a proxy), as well as a restricted network installation.

The typical installation and utilization of this playbook is to launch it from the system architect's laptop, outside of the environment that is desired to be provisioned. The pre-requisite services required are typically hosted on a "bastion" or infrastructure system that hosts system services required by this playbook. It is up to the system architect to provide these services at this time.

## Pre-requisites before you get started

### Services

1. Load your api token on cloud.redhat.com/openshift
   - store it in a text file called "api_token.txt"
2. An available HTTP server, such as Nginx or Apache, deployed and available
   - The following can be used: <https://github.com/sonofspike/http_store>
3. An available container registry if a restricted network installation is desired, to be deployed and available with OpenShift content mirrored to it
   - The following can be used for the mirror itself: <https://github.com/sonofspike/registry_mirror>
   - The following can be used for accomplishing operator-specific mirroring after the registry is stood up: <https://github.com/openshift-telco/ocp4-offline-operator-mirror>

### The Usual OpenShift Infrastructure Requirements
3. NTP server, use chrony 
4. DHCP (dnsmasq) for giving out addresses to nodes that will become part of the cluster
   - Future updates to this playbook will support static IP address assignment
5. API endpoint (API Virtual IP)
6. Wildcard domain `*.apps.<clusterName>.<baseDomain>` (Ingress VIP)

### Files to have available for the playbook

You can check the file prerequisites have been fulfilled by running `ansible-playbook -i localhost, prerequisites.yml`.

1. Your OpenShift pull secret <https://cloud.redhat.com/openshift/install>
   - Store this as `pull_secret.txt` in the playbook base directory
2. Your SSH Public Key that will be injected into the nodes `~/.ssh/authorized_keys` directory
   - Store this as `ssh_public_key.txt` in the playbook base directory
3. The trusted SSL signed self-certificate to be used for the registry, which must be injected into the installation as a trusted repository
   - Store this as `mirror_certificate.txt` in the playbook base directory. Do not forget to pad this entire file with four spaces for every line, even the BEGIN and END CERTIFICATE lines

## Running

When you're ready to execute this, do the following

1. Modify the provided `inventory` file. Add appropriate values that suit your environment in the various sections
2. Modify `deploy_cluster.yml` and input the Assisted Installer Host and port that matches your environment

The following command launches the playbook:

```sh
ansible-playbook -i inventory deploy_cluster.yml
```
