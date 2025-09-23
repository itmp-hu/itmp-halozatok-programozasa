from netmiko import ConnectHandler

s1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
s2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }
s3 = {'device_type': 'cisco_ios','host': '10.0.0.4','username': 'admin','password': 'cisco' }
switchlist = [s1, s2, s3]

for switch in switchlist:
    k = ConnectHandler(**switch)
    output = k.send_command('show spanning-tree | include Root FWD')
    if output != '':
        port = output.split()[0]
        nev = k.find_prompt()[0:-1]
        print('A root port a '+nev+' switchen: '+port)
    k.disconnect()
