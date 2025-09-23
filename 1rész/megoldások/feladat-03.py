from netmiko import ConnectHandler

r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }
r3 = {'device_type': 'cisco_ios','host': '10.0.0.66','username': 'admin','password': 'cisco' }
rlist = [r1, r2, r3]

for rtr in rlist:
    k = ConnectHandler(**rtr)
    print("Hosztnév: ",k.find_prompt()[0:-1], end=',')

    output = k.send_command("show run | include auto-cost")
    if output == '':
        cref = '100'
    else:
        cref=output.split()[2]
    print(cref+' Mbps')
    ref = int(cref)*10
    k.send_config_set(['router ospf 1','auto-cost reference-bandwidth '+str(ref)])
    k.disconnect()




