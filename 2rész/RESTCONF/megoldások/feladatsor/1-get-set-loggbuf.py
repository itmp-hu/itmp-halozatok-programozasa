import json
import requests
requests.packages.urllib3.disable_warnings()

url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/logging/"

fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }

auth = ("admin", "cisco")

output = requests.get(url, auth=auth, headers=fejlec, verify=False)

try:
    outdict = output.json()
    print(json.dumps(outdict, indent=3))
except:
    print("Nem jó...nincs beállítva?")


adat={ "Cisco-IOS-XE-native:buffered" : {
        "size-value" : 10000,
        "severity-level" : "errors" }
       }
adatj = json.dumps(adat)
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/logging/buffered"
output = requests.put(url, auth=auth, data=adatj, headers=fejlec, verify=False)
print(output.status_code)
