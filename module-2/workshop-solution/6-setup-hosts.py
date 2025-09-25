import json
import requests
requests.packages.urllib3.disable_warnings()
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
# az URL végén lévő host-list egy lista objektum:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/host/host-list"
# lekezeljük azt, ha még nincsenek host bejegyzések:
output = requests.get(url, auth=auth, headers=fejlec, verify=False)
try:
    print(json.dumps(output.json(), indent=4))
except:
    print("még nincsenek bejegyzések...")

# új bejegyzések létrehozásához, a feltöltéshez most a szülő konténert kell megadni, aminek URL-je:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/host"
# a szótár kulcsa magára a listára mutat, amibe az adatok kerülnek:
adat = {
    "Cisco-IOS-XE-native:host-list": [
        {
            "name": "pc2",
            "ip-list": [
                "1.1.1.2"
            ]
        },
      {
            "name": "pc3",
            "ip-list": [
                "1.1.1.3"
            ]
        }  
    ]
}
adatj = json.dumps(adat)
# a POST metódust kell használni új objektumok létrehozásához:
output = requests.post(url, auth=auth, headers=fejlec, data=adatj, verify=False)
print(output.status_code)
