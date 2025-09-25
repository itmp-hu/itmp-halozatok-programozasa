import json
import requests
# letiltjuk a fölösleges figyelmeztetéseket:
requests.packages.urllib3.disable_warnings()

# beállítjuk a YANG modell alapján az URL-t, majd a szükséges fejléc- és hitelesítő adatokat:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/logging/"
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
# elküldjük a GET kérést:
output = requests.get(url, auth=auth, headers=fejlec, verify=False)
# ha nincs beállítva, akkor kivételkezeléssel akadályozzuk meg a program leállását: 
try:
    outdict = output.json()
    print(json.dumps(outdict, indent=3))
except:
    print("Nem jó...nincs beállítva?")

# az új érték beállításához összeállítjuk egy szótárban a szükséges adatokat, ismét a YANG modell alapján:
adat={ "Cisco-IOS-XE-native:buffered" : {
        "size-value" : 10000,
        "severity-level" : "errors" }
       }
# a szótárat átalakítjuk JSON formátumra:
adatj = json.dumps(adat)
# megadjuk a módosításhoz az URL-t, és a PUT metódussal el is végezzük azt:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/logging/buffered"
output = requests.put(url, auth=auth, data=adatj, headers=fejlec, verify=False)
# lekérjük az állapotkódot:
print(output.status_code)
