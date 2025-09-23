from netmiko import ConnectHandler
import re

sw = { 
    'device_type': 'cisco_ios',
    'host': '10.0.0.4',
    'username': 'admin',
    'password': 'cisco',}

k = ConnectHandler(**sw)

output = k.send_command('show vlan brief | inc 10')
# hogy néz ki a nyers formátumú kimenet?
# print(repr(output))

for sor in output.splitlines():
    o = re.search("^10\s", sor)
    if o:
        n1 = sor.split()[1]
        if n1 != 'WORK':
            ki = k.send_config_set(["vlan 10","name WORK"])
            print(ki)
k.disconnect()
