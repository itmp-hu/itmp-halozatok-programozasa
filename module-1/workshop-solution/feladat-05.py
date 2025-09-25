from netmiko import ConnectHandler

s1 = {'device_type': 'cisco_ios','host': '10.0.0.4','username': 'admin','password': 'cisco' }

v = input('Melyik VLAN tagjait keressük: ')

k = ConnectHandler(**s1)
# a megfelelő show parancs kimenetét sorokra bontjuk:
output = k.send_command('show interfaces status')
for sor in output.splitlines():
    # ha nem üres a sor, akkor szavakra bontjuk:
    if sor != '':
        sor = sor.split()
        # ha a VLAN azonosítót tartalmazó szó megegyezik a keresettel, kiírjuk:
        if sor[2] == v:
            print(sor[0])
    
k.disconnect()


