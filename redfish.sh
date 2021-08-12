export bmc=10.198.0.64
export token=`curl -k -H "Content-Type: application/json" -X POST https://${bmc}/login -d '{"username" :  "USERID", "password" :  "PASSW0RD"}' | grep token | awk '{print $2;}' | tr -d '"'`
curl -k -H "X-Auth-Token: $token" https://${bmc}/redfish/v1/...
curl -k -X GET https://10.198.0.64/login -d '{"username" :  "USERI


curl -d '{"Boot":{"BootSourceOverrideEnabled":"Disabled","BootSourceOverrideMode":"UEFI","BootSourceOverrideTarget":"Hdd","UefiTargetBootSourceOverride":null}}' -H "Content-Type: application/json" -X PATCH https://10.198.0.64/redfish/v1/Systems/1 --insecure -u USERID:PASSW0RD

curl -d '{"Image": "https://10.198.7.130:8080/opt/http_store/data/discovery-image-4.8.iso, "Inserted": true}' -H "Content-Type: application/json" -X PATCH https://10.198.0.64/redfish/v1/Managers/1/VirtualMedia/EXT1 --insecure -u USERID:PASSW0RD

curl -H "Content-Type: application/json" -X GET https://10.198.0.64/redfish/v1/Managers/1 --insecure -u USERID:PASSW0RD | jq 
curl -H "Content-Type: application/json" -X GET https://10.198.0.64/redfish/v1/Managers/1/VirtualMedia --insecure -u USERID:PASSW0RD | jq 
curl -H "Content-Type: application/json" -X GET https://10.198.0.64/redfish/v1/Managers/1/VirtualMedia/EXT1 --insecure -u USERID:PASSW0RD | jq 
