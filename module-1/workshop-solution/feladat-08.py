from netmiko import ConnectHandler
# használjunk reguláris kifejezést a pontos szövegkereséshez:
import re

sw = { 
    'device_type': 'cisco_ios',
    'host': '10.0.0.4',
    'username': 'admin',
    'password': 'cisco',}

k = ConnectHandler(**sw)
# hogy kevesebb adattal kelljen dolgozni, csak a 10 szövegrészletet tartalmazó kimenetet kérjük:
output = k.send_command('show vlan brief | inc 10')

for sor in output.splitlines():
    # a pontos egyezést reguláris kifejezéssel adjuk meg: a sor elején (^) keresünk 1, majd 0 karaktereket, amiket whitespace(ek) (\s) követ(nek):
    o = re.search("^10\s", sor)
    # ha van találat, és a VLAN neve nem WORK, akkor beállítjuk arra:
    if o:
        n1 = sor.split()[1]
        if n1 != 'WORK':
            ki = k.send_config_set(["vlan 10","name WORK"])
            print(ki)
k.disconnect()
