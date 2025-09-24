import requests
import json
USER = 'admin'
PASS = 'cisco'
# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()

#
# A napi üzenet példáján keresztül a 4 alapművelet:
#
# lekérdezés:
url = "https://192.168.122.122/restconf/data/Cisco-IOS-XE-native:native/banner/motd/banner"
headers = { 'Accept': "application/yang-data+json",'Content-Type': "application/yang-data+json"  }

response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
if response.text == "":
    print("not set yet")
else:
    print(response.text)
    print("Másképpen: ")
    print(json.dumps(response.json(), indent=3))

## új készítése
# az URL a szülő, tároló objektumra mutat:
url = "https://192.168.122.122/restconf/data/Cisco-IOS-XE-native:native/banner/motd/"
# ebbe kell elhelyezni egy szótárat az új értékkel:
adat = { "banner" : "1 first RESTCONF banner 1" }
# teljesen új beállítás, ezért POST:
response = requests.post(url, auth=(USER, PASS), data=json.dumps(adat), headers=headers, verify=False)
print("Létrehozás kódja: ",response.status_code, response.text)

x = input("Pause...")

### módosítás:
# az URL a módosítandó objektumra mutat:
url = "https://192.168.122.122/restconf/data/Cisco-IOS-XE-native:native/banner/motd/banner"
adat = { "banner" : "1 second RESTCONF banner 1" }
# módosítás, tehát PUT vagy PATCH
response = requests.patch(url, auth=(USER, PASS), data=json.dumps(adat), headers=headers, verify=False)
print("Módosítás kódja: ",response.status_code, response.text)

x = input("Pause...")

## törlés:
# az URL a törlendő objektumra mutat:
url = "https://192.168.122.122/restconf/data/Cisco-IOS-XE-native:native/banner/motd/banner"
response = requests.delete(url, auth=(USER, PASS), headers=headers, verify=False)
print("Törlés kódja: ",response.status_code)
