from netmiko import ConnectHandler

def setIPtoInterface(device_params, interface, ip, subnet):
    with ConnectHandler(**device_params) as ssh:
        ssh.config_mode()
        commands = [
            "int {}".format(interface),
            "ip add {} {}".format(ip, subnet),
            "no shut",
        ]
        ssh.send_config_set(commands)
        ssh.exit_config_mode()
        ssh.save_config()
        ssh.disconnect()

def main():
    device_ip = "10.0.15.102"
    username = "admin"
    password = "cisco"

    device_params = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
    }
    result = setIPtoInterface(device_params, "lo60070069", "192.168.1.1", "255.255.255.0")
    
main()