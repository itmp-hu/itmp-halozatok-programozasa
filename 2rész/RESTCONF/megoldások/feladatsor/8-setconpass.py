import requests
import json
USER = 'admin'
PASS = 'cisco'
# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()
headers = { 'Accept': "application/yang-data+json",'Content-Type': "application/yang-data+json"  }

url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0/password"
adat = '''
{ "secret" : "conpass" }
'''
response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
print(response.status_code, response.text)

url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0"
adat = '''
{ "login" : {} }
'''
response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
print(response.status_code, response.text)

url = "https://192.168.122.150/restconf/data/Cisco-IOS-XE-native:native/line/console=0/logging"
adat = '''
{ "synchronous" : {} }
'''
response = requests.post(url, auth=(USER, PASS), data=adat, headers=headers, verify=False)
print(response.status_code, response.text)

