from netmiko import ConnectHandler

r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }

rlist = [r1, r2 ]

for rtr in rlist:
    k = ConnectHandler(**rtr)
    print("Hosztnév: ",k.find_prompt()[0:-1], end=',')
    # lekérdezzük az aktuális beállítást a futó konfigurációból:
    output = k.send_command("show run | include auto-cost")
    # ha nem kapun vissza értéket, akkor az alapértelmezett 100 van érvényben:
    if output == '':
        cref = '100'
    # egyébként pedig a kimenetet szétbontjuk, és az így kapott lista 2. indexű eleme a keresett érték:
    else:
        cref=output.split()[2]
    print(cref+' Mbps')
    # számmá alakítjuk és kiszámítjuk az új értéket:
    ref = int(cref)*10
    # végül kiadjuk a megfelelő konfigurációs parancsot (stringgé való visszaalakítás is kell):
    k.send_config_set(['router ospf 1','auto-cost reference-bandwidth '+str(ref)])
    k.disconnect()




