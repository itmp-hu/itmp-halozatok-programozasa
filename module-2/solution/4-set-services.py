import json
import requests
requests.packages.urllib3.disable_warnings()
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/service/password-encryption"

adat = { "Cisco-IOS-XE-native:password-encryption": [ "" ] }
adatj = json.dumps(adat)

output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
print(output.status_code)

output = requests.get(url, auth=auth, headers=fejlec, verify=False)
print(json.dumps(output.json(), indent=4))



