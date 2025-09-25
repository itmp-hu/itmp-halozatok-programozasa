import requests
import json
USER = 'admin'
PASS = 'cisco'
# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()
headers = { 'Accept': "application/yang-data+json",'Content-Type': "application/yang-data+json"  }

# a line konténerben lévő console egy lista, aminek 0-ás kódú elemét választjuk ki, ennek pedig password konténerét:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0/password"
# ezen belül a secret nevű leaf objektumot kell adattal feltölteni:
adat = '''
{ "secret" : "conpass" }
'''
# POST metódus kell a módosításhoz:
response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
print(response.status_code, response.text)

# a jelszót be is kell kérni, tehát kell még a login parancs is, ezért újra kiválasztjuk a konzolt:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0"
# a login egy konténerként van definiálva, ez tulajdonképpen egy szótárnak felel meg, ami jelen esetben üres:
adat = '''
{ "login" : {} }
'''
response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
print(response.status_code, response.text)

# a synchronous szintén egy konténer, az előbbi módszerrel álítjuk be őt is:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0/logging"
adat = '''
{ "synchronous" : {} }
'''
response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
print(response.status_code, response.text)
