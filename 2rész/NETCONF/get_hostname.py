from ncclient import manager
import xmltodict
import xml.dom.minidom

m = manager.connect(host='192.168.122.150', port=830, username='admin',
                    password='cisco', device_params={'name': 'csr'})

running_config = m.get_config('running')

conf_json = xmltodict.parse(str(running_config))

print("A hosztnév: ",conf_json['rpc-reply']["data"]["native"]["hostname"])

m.close_session()
