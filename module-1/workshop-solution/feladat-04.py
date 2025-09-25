from netmiko import ConnectHandler

r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }

rlist = [r1, r2]

for rtr in rlist:
    k = ConnectHandler(**rtr)
    p = k.find_prompt()
    # kigyűjtjük a soros interfészek neveit egy kezdetben üres listába:
    o = k.send_command('sh ip interface brief | include Serial')
    serials = []
    for i in o.splitlines():
        serials.append(i.split()[0])
    # egy következő paranccsal megállapítjuk, melyiken van PPP beágyazási mód:
    for i in serials:
        o = k.send_command('show interfaces '+i+' | include Encapsulation PPP')
        # ha találtunk ilyen interfészt, vagyis a kimenet nem üres, akkor kiíratjuk, melyik eszköz melyik interfésze:
        if o != '':
            print(p,i)
            # végül bekonfiguráljuk:
            k.send_config_set(['interface '+i,'compress predictor'])
    k.disconnect()
