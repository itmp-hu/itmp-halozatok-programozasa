import json
import requests
requests.packages.urllib3.disable_warnings()

url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/hostname"

fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }

auth = ("admin", "cisco")

output = requests.get(url, auth=auth, headers=fejlec, verify=False)

output_json = output.json()
print(output_json)

h = output_json["Cisco-IOS-XE-native:hostname"]
print("Hosztnév: "+h)
