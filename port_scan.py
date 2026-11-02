#file for port scanning
import sys
import socket
from datetime import datetime
 
# Defining a target
target_hostname = socket.gethostname()
target = socket.gethostbyname(target_hostname)


 
try:
    
    # will scan ports between 1 to 65,535
    for port in range(1,65535):
        if port%10 == 0:
              print(f"Sken portu číslo {port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        
        # returns an error indicator
        result = s.connect_ex((target,port))
        if result ==0:
            print("Port {} is open".format(port))
        s.close()
        
except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
except socket.error:
        print("\n Server not responding !!!!")
        sys.exit()
