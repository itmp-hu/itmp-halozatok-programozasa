from ncclient import manager
router = {
   'ip': '192.168.122.150',
   'port': '830',
   'username': 'admin',
   'password': 'cisco'
}
m = manager.connect(host=router['ip'], port=router['port'], username=router['username'],
                    password=router['password'], device_params={'name':'iosxe'}, hostkey_verify=False)

netconf_payload = '''
<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
        <Loopback>
            <name>1</name>
            <ip>
                <address>
                    <primary>
                        <address>1.1.1.1</address>
                        <mask>255.255.255.255</mask>
                    </primary>
                </address>
            </ip>
        </Loopback>
    </interface>
    </native>
</config>
'''
print(netconf_payload)

response = m.edit_config(config=netconf_payload, target="running")
print(response)

m.close_session()
