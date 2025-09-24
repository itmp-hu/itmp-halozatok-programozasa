import json
import requests
requests.packages.urllib3.disable_warnings()

baseurl = "https://192.168.122.150/restconf/data/ietf-interfaces:interfaces"
url = baseurl +"/"

fejlec = { "Accept": "application/yang-data+json",
           "Content-type":"application/yang-data+json" }
auth = ("admin", "cisco")

adat = { "interface" : [
 {      
   "name": "Loopback3",
   "type": "iana-if-type:softwareLoopback",
   "enabled": False,
   "ietf-ip:ipv4": {
      "address": [
            { "ip": "1.1.1.3",
              "netmask": "255.255.255.0" }
            ]
      }
  }
 ]
}
adatj= json.dumps(adat)

output = requests.post(url, headers=fejlec, data=adatj, auth=auth, verify=False)
print(output.status_code, output.text)

x = input("Nyomj ENTER-t:")
output = requests.get(url, headers=fejlec, auth=auth, verify=False)
print(output.text)































