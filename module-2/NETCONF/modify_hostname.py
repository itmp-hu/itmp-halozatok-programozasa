from ncclient import manager
from pprint import pprint

router = {
   'ip': '192.168.122.150',
   'port': '830',
   'username': 'admin',
   'password': 'cisco'
}

h = input("Új hostnév: ")

netconf_payload = '''
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
   <hostname>{}</hostname>
 </native>
</config>
'''.format(h)

print(netconf_payload)

m = manager.connect(host=router['ip'], port=router['port'], username=router['username'],
                    password=router['password'], device_params={'name':'iosxe'}, hostkey_verify=False)

response = m.edit_config(config=netconf_payload, target="running")

print(response)


m.close_session()
