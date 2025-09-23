import json
import requests
requests.packages.urllib3.disable_warnings()
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/dhcp/pool=POOL1"
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")

output = requests.get(url, auth=auth, headers=fejlec, verify=False)
print(json.dumps(output.json(), indent=4))

# uj DNS szerver:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/dhcp/pool=POOL1/dns-server"
payload = '''
{
    "Cisco-IOS-XE-dhcp:dns-server": {
        "dns-server-list": [
            "4.4.4.4",
            "8.8.4.4"
        ]
    }
}
'''
output = requests.put(url, auth=auth, headers=fejlec, data=payload, verify=False)
print(output.status_code)

# masik domain név
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/dhcp/pool=POOL1/domain-name"
d = input("Új domain: ")
payload = {
    "domain-name": d
}
response = requests.patch(url, headers=fejlec, auth=auth, data=json.dumps(payload), verify=False)
print(response.status_code)
