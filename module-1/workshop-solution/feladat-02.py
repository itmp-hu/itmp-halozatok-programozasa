from netmiko import ConnectHandler
# az 1. feladathoz hasonlóan az eszközök adatait felvesszük, és listába rakjuk:
r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }
rlist = [r1, r2 ]

ujkulcs = input("Új OSPF kulcs értéke: ")

for rtr in rlist:
    k = ConnectHandler(**rtr)
    print("Hosztnév: ",k.find_prompt()[0:-1])
    # az OSPF folyamatban részt vevő interfészek listája kezdetben üres:
    intlist = []
    # a megfelelő show parancs kimenetét szétbontjuk sorokra:
    output = k.send_command("show ip ospf interface brief").splitlines()
    # a fejlécet tartalmazó sor utáni összes sorra végrehajtjuk, hogy szavakra bontjuk, és az így előállt lista 0. eleme a keresett interfész neve, amit berakunk a listába:
    for sor in output[1:]:
        intlist.append(sor.split()[0])
    print(intlist)
    # az interfészeket kivesszük a listából, és mindegyikre alkalmazzuk a megfelelő konfigurációt:
    for i in intlist:
        k.send_config_set(["interface "+i, "no ip ospf message-digest 1", \
                           "ip ospf message-digest-key 1 md5 "+ujkulcs])
    k.disconnect()
