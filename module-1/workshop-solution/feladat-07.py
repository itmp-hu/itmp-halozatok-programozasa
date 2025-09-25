from netmiko import ConnectHandler

s1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
s2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }

switchlist = [s1, s2]

for switch in switchlist:
    k = ConnectHandler(**switch)
    # csak a root portok adatait tartalmazó sorban szerepel a Root FWD szöveg:
    output = k.send_command('show spanning-tree | include Root FWD')
    # ha megtaláltuk a kimenetben, akkor a megtalált sort szavakra bontjuk, és a 0. indexű elem lesz a port neve:
    if output != '':
        port = output.split()[0]
        nev = k.find_prompt()[0:-1]
        print('A root port a '+nev+' switchen: '+port)
    k.disconnect()
