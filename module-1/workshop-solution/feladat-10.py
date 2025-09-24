from netmiko import ConnectHandler

s1 = {'device_type': 'cisco_ios','host': '10.0.0.2','username': 'admin','password': 'cisco' }
s2 = {'device_type': 'cisco_ios','host': '10.0.0.3','username': 'admin','password': 'cisco' }
s3 = {'device_type': 'cisco_ios','host': '10.0.0.4','username': 'admin','password': 'cisco' }
switchlist = [s1, s2, s3]

for switch in switchlist:
    k = ConnectHandler(**switch)
    output = k.send_command('show cdp neighbor',use_textfsm=True)
    print(k.find_prompt(),"eszköz switch szomszédai:")
    for e in output:
        if e["capability"] == "S I":
            print(e["neighbor"])
    k.disconnect()
