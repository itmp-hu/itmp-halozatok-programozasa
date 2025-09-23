from netmiko import ConnectHandler

s1 = {'device_type': 'cisco_ios',
      'host': '10.0.0.1',
      'username': 'admin',
      'password': 'cisco',
      'secret': "cisco" }

k = ConnectHandler(**s1)

k.enable()
k.config_mode()
print(k.send_command_expect('crypto key generate rsa', expect_string='replace them'))
print(k.send_command_expect('y\n', expect_string='How many bits'))
print(k.send_command_expect('1024\n', expect_string='#'))
print(k.exit_config_mode())

k.disconnect()
