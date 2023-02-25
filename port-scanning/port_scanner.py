import socket
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# format -> HOST = url to scan; START_PORT = the port to start scanning; END_PORT = the port to end scanning

# Target to scan (no protocol and subdomain)
HOST_IP = '186.192.101.56'
#HOST_IP = socket.gethostbyname(HOST)

# Ports interval
START_PORT = 0
END_PORT = 10000 

# Protocols to connect
TCP_PROTOCOL = True # Scan TCP protocol?
UDP_PROTOCOL = False # Scan UDP protocol?

# File .txt to write the ports
RESULT_LIST = open('port-scanning/openned_ports.txt', 'w+') 

# Reference to the services list by port
html_requested = requests.get('https://www.portalchapeco.com.br/jackson/portas.htm')
html_elements = BeautifulSoup(html_requested.content, 'html.parser')

# Initial values to reference
services_by_ports = [] # Contains dicts that key = current protocol and value = current protocol service
find_ports = 0 
START_TIME = datetime.now()


# Construct the array that contains the dicts { protocol: service } by port scanned
def __build_dict__(port):
    services_by_ports.clear()  
    arrayContent = html_elements.find_all('td', class_ = 'r', string = '{}'.format(port))
    if len(arrayContent) == 0:
        return False

    else:
        for element in arrayContent:      
            ports_dict = {}
            protocol_type = element.find_next_sibling().contents[0]
            service_type = element.find_next_sibling().find_next_sibling().contents              
            if len(service_type) == 0:
                service_type = 'unknown'
            else:
                service_type = service_type[0]  

            ports_dict[str(protocol_type)] = str(service_type)
            services_by_ports.append(ports_dict)
        return True

# Verify if the current protocol has service: if has, returns it, if hasn't, returns 'unknown'
def __verify_service__(protocol):
    if len(services_by_ports) == 1:      
        protocol_in_dict = list(services_by_ports[0].keys())[0]
        service_name = list(services_by_ports[0].values())[0]
        if (protocol_in_dict == 'UDP') and (protocol == 'UDP'):
            return service_name
        elif (services_by_ports[0] == 'UDP') and (protocol == 'TCP'):
            return 'unknown'
        elif (services_by_ports[0] == 'TCP') and (protocol == 'UDP'):
            return 'unknown'
        else:
            return service_name
    else:       
        if protocol == 'TCP':
            return str(services_by_ports[0][protocol])
        else:
            return str(services_by_ports[1][protocol])

# Try to connect to the current port and then, prints the result of connection: 'port/protocol service'
try:
    for port in range(START_PORT, END_PORT):
        print(port)
        the_port_exists = __build_dict__(port)
        if the_port_exists:
            sock_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_udp.settimeout(0.20)
            sock_tcp.settimeout(0.20)
            result_udp = sock_udp.connect_ex((HOST_IP, port))
            result_tcp = sock_tcp.connect_ex((HOST_IP, port)) 
            service_udp = __verify_service__('UDP')
            service_tcp = __verify_service__('TCP')
            udp_full_text = str(port) + '/udp ' + service_udp
            tcp_full_text = str(port) + '/tcp ' + service_tcp    
            if TCP_PROTOCOL and UDP_PROTOCOL:
                if result_udp == 0:
                    print(udp_full_text)
                    RESULT_LIST.write(udp_full_text)
                if result_tcp == 0:
                    print(tcp_full_text)
                    RESULT_LIST.write(tcp_full_text)        
            elif TCP_PROTOCOL:
                if result_tcp == 0:
                    print(tcp_full_text)
                    RESULT_LIST.write(tcp_full_text) 
            elif UDP_PROTOCOL:
                if result_udp == 0:
                    print(udp_full_text)
                    RESULT_LIST.write(udp_full_text)
            else:
                raise Exception

            sock_udp.close()
            sock_tcp.close()
        else:
            continue

# If an error occurs in the try scope, its because no protocol was selected, then print to choose one
except Exception:
    print('You must select a protocol.')

# End of scanning parameters
END_TIME = datetime.now() # Contains the end of scanning 
TOTAL_TIME =  END_TIME - START_TIME # Calculates the total time of scanning
print("Scanning duration: ", TOTAL_TIME) # Prints the total time of scanning
print("Total ports find: ", find_ports) # Prints the total ports openned