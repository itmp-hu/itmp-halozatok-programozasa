from netmiko import ConnectHandler

r1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
r2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }
r3 = {'device_type': 'cisco_ios','host': '10.0.0.4','username': 'admin','password': 'cisco' }
rlist = [r1, r2, r3]

for rtr in rlist:
    k = ConnectHandler(**rtr)
    output = k.send_command('show spanning-tree')
    for sor in output.splitlines():
        if 'This bridge is the root' in sor:
            rootbr = k.find_prompt()[0:-1]
            rootcim = k.host
            break
    
    k.disconnect()

print(f'A root bridge: {rootbr}, IP-címe: {rootcim}')
