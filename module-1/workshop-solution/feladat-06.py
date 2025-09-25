from netmiko import ConnectHandler

s1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
s2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }

slist = [s1, s2]

for sw in slist:
    k = ConnectHandler(**sw)
    output = k.send_command('show spanning-tree')
    for sor in output.splitlines():
        # ha a show parancs kimenetében megvan a keresett szöveg, akkor kiírjuk az állomásnevet és IP címet is:
        if 'This bridge is the root' in sor:
            rootbr = k.find_prompt()[0:-1]
            rootcim = k.host
            # ha megtaláltuk a root bridge-et, nem nézzük meg a többi switch-et:
            break
    
    k.disconnect()
# az eredményt formázottan kiírjuk:
print(f'A root bridge: {rootbr}, IP-címe: {rootcim}')
