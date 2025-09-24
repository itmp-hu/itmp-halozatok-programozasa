from netmiko import ConnectHandler

r1 = {'device_type': 'cisco_ios','host': '10.0.0.4','username': 'admin','password': 'cisco' }

v = input('Melyik VLAN tagjai: ')

k = ConnectHandler(**r1)
output = k.send_command('show interfaces status')
for sor in output.splitlines():
    if sor != '':
        sor = sor.split()
        if sor[2] == v:
            print(sor[0])
    
k.disconnect()


