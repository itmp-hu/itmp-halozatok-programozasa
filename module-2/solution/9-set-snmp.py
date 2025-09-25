import json
import requests
requests.packages.urllib3.disable_warnings()

baseurl = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native"
url = baseurl +"/snmp-server"

fejlec = { "Accept": "application/yang-data+json",
           "Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")

# A native modul nem tartalmazza a szükséges beállításokat, hanem szükség van a Cisco-IOS-XE-snmp modulra is, mint kibővítés (augment).
# Egyszerűsítésként állítsuk be előzetesen manuálisan az SNMP-t, kérdezzük le a fenti URL segítségével, és ebből vehetjük, hogy kell kinéznie az elküldendő adatoknak:
adat = '''
{
  "Cisco-IOS-XE-native:snmp-server": {
    "Cisco-IOS-XE-snmp:community-config": [
      {
        "name": "titkos",
        "permission": "rw"
      },
      {
        "name": "nyilvanos",
        "permission": "ro"
      }
    ],
    "Cisco-IOS-XE-snmp:contact": "Teszt Elek"
  }
}
'''
output = requests.put(url, headers=fejlec, data=adat, auth=auth, verify=False)
print(output.status_code)

output = requests.get(url, headers=fejlec, auth=auth, verify=False)
print(output.text)































