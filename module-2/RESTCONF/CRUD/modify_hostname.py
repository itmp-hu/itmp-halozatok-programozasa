import json
import requests
requests.packages.urllib3.disable_warnings()
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/hostname"
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
ujnev = input("Új hosztnév: ")
body = '{"hostname": "'+ujnev+'"}'

output = requests.put(url, auth=auth, headers=fejlec, data=body, verify=False)
print(output.status_code)

output = requests.get(url, auth=auth, headers=fejlec, verify=False)
print(output.text)

