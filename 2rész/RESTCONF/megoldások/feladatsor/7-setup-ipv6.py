import json
import requests
requests.packages.urllib3.disable_warnings()
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ipv6/unicast-routing"

adat = '''
{
    "Cisco-IOS-XE-native:unicast-routing": [
        ""
    ]
}
'''
output = requests.put(url, auth=auth, headers=fejlec, data=adat, verify=False)
if output.status_code < 300:
    print("Sikeres.")
    

