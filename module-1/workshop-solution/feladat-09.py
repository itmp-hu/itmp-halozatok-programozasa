from netmiko import ConnectHandler

r1 = {'device_type': 'cisco_ios',
      'host': '10.0.0.1',
      'username': 'admin',
      'password': 'cisco',
      'secret': "cisco" }

k = ConnectHandler(**r1)
# most nem alkalmazhatjuk a send_config_set() metódust, ezért "kézzel" lépünk be globális konfig módba:
k.enable()
k.config_mode()
# kiadjuk a parancsot, amire megvárjuk, míg a routeren megjelenik a "replace them" szöveg:
print(k.send_command_expect('crypto key generate rsa', expect_string='replace them'))
# igennel (y) válaszolunk, erre megvárjuk, míg megjelenik a bitek számára vonatkozó kérdés:
print(k.send_command_expect('y\n', expect_string='How many bits'))
# beadjuk az értéket, amire a parancs lefut és vissza kell kapnunk a promtot, a végén hashtaggel:
print(k.send_command_expect('1024\n', expect_string='#'))
# kilépünk és kijelentkezünk:
print(k.exit_config_mode())

k.disconnect()
