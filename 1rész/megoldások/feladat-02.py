from netmiko import ConnectHandler

r1 = {'device_type': 'cisco_ios','host': '10.0.0.1','username': 'admin','password': 'cisco' }
r2 = {'device_type': 'cisco_ios','host': '10.0.0.65','username': 'admin','password': 'cisco' }
r3 = {'device_type': 'cisco_ios','host': '10.0.0.66','username': 'admin','password': 'cisco' }
rlist = [r1, r2, r3]

ujkulcs = input("Új OSPF kulcs értéke: ")

for rtr in rlist:
    k = ConnectHandler(**rtr)
    print("Hosztnév: ",k.find_prompt()[0:-1])
    intlist = []
    output = k.send_command("show ip ospf interface brief").splitlines()
    for sor in output[1:]:
        intlist.append(sor.split()[0])
    print(intlist)
    for i in intlist:
        k.send_config_set(["interface "+i, "no ip ospf message-digest 1", \
                           "ip ospf message-digest-key 1 md5 "+ujkulcs])
    k.disconnect()
