import socket
import subprocess
import re


class PC:
    def __init__(self): 
        self.name = socket.gethostname()
        self.ipv4 = None
        self.ipv6 = None
        self.dns_servery = []
        self.gateway_ip = None
        self.subnet_mask = None
    
    def get_network_info(self):
        info = subprocess.run(["ipconfig", "/all"],capture_output=True,text=True)
        return info.stdout

    def is_connected(self):
        try:
            socket.gethostbyname("google.com")
            return True
        except Exception:
            return False

    def collect(self):
        if self.is_connected():
            self.ipv4 = socket.gethostbyname(self.name)

            data = self.get_network_info()

            #Získání IPv6 adresy
            match = re.search(r"IPv6 Address.*?:\s*([a-fA-F0-9:]+)", data)
            self.ipv6 = match.group(1) if match else None

            #Získání subnet masky
            match = re.search(r"Subnet Mask.*?:\s*([\d\.]+)", data)
            self.subnet_mask = match.group(1) if match else None

            #Získání default gateway
            match = re.search(r"Default Gateway.*?:\s*([\d\.]+)", data)
            self.gateway_ip = match.group(1) if match else None

            #Získání adres a jmen DNS serverů
            self.dns_servery = self.get_dns_servers()

    def get_dns_servers(self):
        data = self.get_network_info().splitlines()
        dns_list = []
        collecting = False

        for line in data:
            if "DNS Servers" in line:
                collecting = True
                value = line.split(":", 1)[1].strip()
                dns_list.append(value)
            elif collecting:
                if line.startswith(" "):
                    dns_list.append(line.strip())
                else:
                    collecting = False

        result = []
        for entry in dns_list:
            try:
                ip = socket.gethostbyname(entry)
                result.append((entry, ip))
            except:
                result.append((None, entry))

        return result




