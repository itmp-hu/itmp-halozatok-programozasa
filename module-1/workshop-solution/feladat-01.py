from netmiko import ConnectHandler
# felvisszük az eszközök adatait egy-egy szótárba, ügyelve az IP címekre és belépési adatokra:
r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }

# betesszük őket egy listába:
rlist = [r1, r2 ]

# egy ciklusban sorban kapcsolódunk hozzájuk:
for rtr in rlist:
    k = ConnectHandler(**rtr)
    print("Hosztnév: ",k.find_prompt()[0:-1], end=',')
    # a megfelelő show paranccsal kiíratjuk a router-ID-t tartalmazó sort:
    output = k.send_command("show ip ospf | include ID")
    # a kimenetet szétbontjuk és egy listát kapunk:
    line = output.split()
    # a keresett ID a lista 6. indexű eleme:
    ospfid = line[6]
    print(" OSPF ID: ",ospfid)
    k.disconnect()
