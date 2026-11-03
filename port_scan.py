#file for port scanning
import sys
import socket
from datetime import datetime

def run_port_scan(target_ip, min:int, max:int)->list[int]:
        open_ports:int=[]
        closed_ports:int=[]
        try:
                for port in range(min, max+1):
                        print(f"Scan portu číslo {port}")
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socket.setdefaulttimeout(1)
                               
                        # returns an error indicator
                        result = s.connect_ex((target_ip,port))
                        if result ==0:
                                print(f"Port č.{port} je otevřený")
                                open_ports.append(port)
                                s.close()
                        else:
                                closed_ports.append(port)
                                print(f"Port č.{port} je zavřený")
                                s.close()
        except KeyboardInterrupt:
                print("\n Opouštění programu")
                sys.exit()
        except socket.gaierror:
                print("\n Hostname Could Not Be Resolved")
                sys.exit()
        except socket.error:
                print("\n Server neodpovídá")
                sys.exit()
        
        return open_ports,closed_ports

#run_port_scan('10.215.250.227',140,150)
