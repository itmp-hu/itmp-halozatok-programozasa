import requests
import json

USER = 'admin'
PASS = 'cisco'

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()

url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1"

headers = {
    'Accept': "application/yang-data+json",
    'Content-Type': "application/yang-data+json",
    'cache-control': "no-cache",
    }

response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
print(response.text)
