import json
import requests
requests.packages.urllib3.disable_warnings()
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/ftp/username"

adat = { "Cisco-IOS-XE-native:username": "ftpuser" }
adatj = json.dumps(adat)

output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
print(output.status_code)

output = requests.get(url, auth=auth, headers=fejlec, verify=False)
print(json.dumps(output.json(), indent=4))

######
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/ftp/password/password-container/password"
adat = { "Cisco-IOS-XE-native:password": "ftppass" }
adatj = json.dumps(adat)

output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
print(output.status_code)

output = requests.get(url, auth=auth, headers=fejlec, verify=False)
print(json.dumps(output.json(), indent=4))
