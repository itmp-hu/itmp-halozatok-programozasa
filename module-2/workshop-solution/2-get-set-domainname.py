import json
import requests
requests.packages.urllib3.disable_warnings()
# megkeressük a megfelelő URL-t, esetünkben ez a következő:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/domain/name"

fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")

# az előzetesen definiált adatokkal elküldjük a GET kérést:
output = requests.get(url, auth=auth, headers=fejlec, verify=False)
# lekezeljük, ha esetleg nincs beállítva semmilyen érték:
try:
    outdict = output.json()
    print(json.dumps(outdict, indent=3))
except:
    print("Nem jó...nincs beállítva?")

# az új értéket egy szótárban definiáljuk, amit JSON formátumra alakítunk:
adat={ "Cisco-IOS-XE-native:name" : "proba.lan"  }
adatj = json.dumps(adat)

# a PUT metódussal küldjük el a módosítandó adatokat, majd lekérdezzük az állapotkódot:
output = requests.put(url, auth=auth, data=adatj, headers=fejlec, verify=False)
print(output.status_code)
