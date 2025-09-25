import json
import requests
requests.packages.urllib3.disable_warnings()
fejlec = { "Accept": "application/yang-data+json","Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")
# a unicast-routing egy leaf objektum:
url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/ipv6/unicast-routing"

# a bekapcsoláshoz itt is egy nullsztringet tartalmazó listát adunk át, az adat többsoros szöveg:
adat = '''
{
    "Cisco-IOS-XE-native:unicast-routing": [""]
}
'''
# a módosításhoz PUT metódus szükséges:
output = requests.put(url, auth=auth, headers=fejlec, data=adat, verify=False)
# ha az állapotkód 300-nál kisebb, akkor a művelet sikeres:
if output.status_code < 300:
    print("Sikeres.")
    

