import json
import requests
requests.packages.urllib3.disable_warnings()
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
# a felhasználónév egy leaf objektum:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/ftp/username"
# definiáljuk az új értéket, JSON formátumra alakítjuk, meghívjuk a PUT metódust a beállításhoz, majd ellenőrizzük:
adat = { "Cisco-IOS-XE-native:username": "ftpuser" }
adatj = json.dumps(adat)

output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
print(output.status_code)

output = requests.get(url, auth=auth, headers=fejlec, verify=False)
print(json.dumps(output.json(), indent=4))

# a jelszó egy másik konténer alatt található:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ip/ftp/password/password-container/password"
adat = { "Cisco-IOS-XE-native:password": "ftppass" }
adatj = json.dumps(adat)
# a beállítás és ellenőrzés hasonló módon történik:
output = requests.put(url, auth=auth, headers=fejlec, data=adatj, verify=False)
print(output.status_code)

output = requests.get(url, auth=auth, headers=fejlec, verify=False)
print(json.dumps(output.json(), indent=4))
