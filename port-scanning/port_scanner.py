from bs4 import BeautifulSoup
from re import search
import requests
import signal
import socket
import time
import sys


shell_list = sys.argv

filename = sys.argv[0]

html_requested = requests.get("https://www.portalchapeco.com.br/jackson/portas.htm")
html_elements = BeautifulSoup(html_requested.content, "html.parser")

services_by_ports = []
find_ports = 0 

START_TIME = time.localtime().tm_sec


# handle the "ctrl + c" command => void
def handle_exit(signal_received, frame):
    print("Scanning finshed with success.")
    show_scanning_time()   


# show time of scanning and then finish the program
def show_scanning_time():
    END_TIME = time.localtime().tm_sec
    TOTAL_TIME =  END_TIME - START_TIME
    formatted_seconds = "{:.3f}s".format(TOTAL_TIME)

    print("Scanning duration: ", formatted_seconds)
    print("Total ports find: ", find_ports)
    sys.exit()


# handle the "--help" argument => void
def help():
    print("\n   Sintax: python3 -u filename.py [HOST] [-t(DEFAULT)] [-u] [-i] [STARTPORT-ENDPORT] [-p] [PORT]\n")
    print("      -t    Allows TCP protocol")
    print("      -u    Allows UDP protocol")
    print("      -i    Especifies that the IPV4 address is not of a website\n")
    sys.exit()


# extract the "startport-endport" interval => ports_interval | False
def return_ports_interval_if_has(argument):
    interval = search(r"[0-9]+[-][0-9]+", argument)
    if bool(interval):
        return str(argument)
    return False


# verify if the argument list has not the "-i" specification => bool
def arguments_has_not_ip_specification(shell_list):
    if not '-i' in shell_list:
        return True
    return False


# verify if the domain argument has not protocol => bool
def domain_name_has_not_protocol(argument):
    if not ("http://" in argument) and not ("https://" in argument):
        return True
    return False


# verify if the current argument is an ip address or domain => bool
def current_argument_is_domain(argument):
    ports_interval = return_ports_interval_if_has(argument)
    if bool(ports_interval):
        if argument != "-t" and argument != "-u" and argument != filename and argument != ports_interval:
            return True
        return False
    elif argument != "-t" and argument != "-u" and argument != filename:
        return True
    return False


# verify if the domain name has the http protocol => bool
def domain_has_http_protocol(host_domain):
    if "http://" in host_domain:
        return True
    return False


# verify if the domain name has the https protocol => bool
def domain_has_https_protocol(host_domain):
    if "https://" in host_domain:
        return True
    return False


# verify what type of target is: ip address, domain, or invalid address => string (hostname or ip)
def get_host_to_scan(shell_list):
    try:
        for argument in shell_list:
            argument = str(argument)
            host_ip = search(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", argument)
            if bool(host_ip):
                if arguments_has_not_ip_specification(shell_list):
                    request_result_https = requests.get("https://" + argument)
                    request_result_http = requests.get("http://" + argument)
                    if request_result_https.status_code != 200:
                        if request_result_http.status_code != 200:
                            print("toaq no if")
                            raise Exception               
                    return argument
                else:
                    return argument
            elif domain_name_has_not_protocol(argument) and current_argument_is_domain(argument):
                raise Exception
            elif current_argument_is_domain(argument):
                host_domain = str(argument)
                request_result = requests.get(host_domain) 
                if request_result.status_code != 200:
                    raise Exception
                else:
                    if domain_has_http_protocol(host_domain):
                        host_domain = host_domain.replace("http://", "")
                    elif domain_has_https_protocol(host_domain):
                        host_domain = host_domain.replace("https://", "")
                    return socket.gethostbyname(host_domain)
    except Exception:
        print("Invalid host name. Example: 'protocol://subdomain.domain.tlds' or")
        sys.exit()
    


# return the extracted interval as a tuple: (start_port, end_port) => (int, int) 
# if hasn't an interval, returns the default interval: (1, 1001), don't includes the last 
def get_ports_to_scan(shell_list):
    for argument in shell_list:
        ports_interval = return_ports_interval_if_has(argument)
        if bool(ports_interval):
            interval_list = ports_interval.split("-")
            start_port = str(interval_list[0])
            end_port = str(interval_list[1])
            return int(start_port), int(end_port) + 1
        else:
            continue
    return 0, 1001


# verify if the arguments list has the "-t" command => bool
# if no protocol argument has specified ("-t" and "-u"), returns "tcp = true", thats the default scan
def tcp_is_selected(shell_list):
    try:
        list(shell_list).index("-t")
        return True
    except ValueError:
        if not udp_is_selected(shell_list):
            return True
        return False
    

# verify if the arguments list has the "-u" command => bool
def udp_is_selected(shell_list):
    try:
        list(shell_list).index("-u")
        return True
    except ValueError:
        return False


# return the protocols to scan as a tuple (tcp, udp) => (bool, bool)
def get_protocols_to_scan(shell_list):
    tcp_protocol = tcp_is_selected(shell_list)
    udp_protocol = udp_is_selected(shell_list)
    return tcp_protocol, udp_protocol



def port_is_documented(port_cell_elements):
    number_of_port_cell = len(port_cell_elements)
    if number_of_port_cell:
        return True
    return False



def port_has_not_service(service_type):
    number_of_service = len(service_type)
    if number_of_service:
        return False
    return True


# handle with data collected by a online documentation of services by port
# can found the documentation accessing: "https://www.portalchapeco.com.br/jackson/portas.htm"
def organize_data_in_dict(port):
    global services_by_ports
    services_by_ports.clear()  
    port_cell_elements = html_elements.find_all("td", class_ = "r", string = "{}".format(port))
    if port_is_documented(port_cell_elements):
        for port_cell in port_cell_elements:      
            ports_dict = {}
            protocol_cell = port_cell.find_next_sibling()
            protocol_type = protocol_cell.contents[0]
            service_cell = protocol_cell.find_next_sibling()
            service_list = service_cell.contents              
            if port_has_not_service(service_list):
                service = "unknown"
            else:
                service = service_list[0]  
            ports_dict[str(protocol_type)] = str(service)
            services_by_ports.append(ports_dict)
        return True
    return False


# returns the service running in each port, if the port is openned and hasn't a service documented, return "unknown"
def return_service_by_port(protocol):
    if len(services_by_ports) == 1:      
        protocol_in_dict = list(services_by_ports[0].keys())[0]
        service_name = list(services_by_ports[0].values())[0]
        if (protocol_in_dict == "UDP") and (protocol == "UDP"):
            return service_name
        elif (services_by_ports[0] == "UDP") and (protocol == "TCP"):
            return "unknown"
        elif (services_by_ports[0] == "TCP") and (protocol == "UDP"):
            return "unknown"
        else:
            return service_name
    else:       
        if protocol == "TCP":
            return str(services_by_ports[0][protocol])
        else:
            return str(services_by_ports[1][protocol])


# try to connect sockets with the range of ports (start_port, end_port) => void
def connect_socket_to_ports(host, tcp_protocol, udp_protocol, start, end):
    global find_ports
    try:
        for port in range(start, end):
            the_port_exists = organize_data_in_dict(port)
            if the_port_exists:
                sock_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_udp.settimeout(0.20)
                sock_tcp.settimeout(0.20)
                result_udp = sock_udp.connect_ex((host, port))
                result_tcp = sock_tcp.connect_ex((host, port)) 
                service_udp = return_service_by_port("UDP")
                service_tcp = return_service_by_port("TCP")
                udp_full_text = str(port) + "/udp " + service_udp
                tcp_full_text = str(port) + "/tcp " + service_tcp    
                if tcp_protocol and udp_protocol:
                    if result_udp == 0:
                        print(udp_full_text)
                        find_ports += 1
                    if result_tcp == 0:
                        print(tcp_full_text)
                        find_ports += 1        
                elif tcp_protocol:
                    if result_tcp == 0:
                        print(tcp_full_text)
                        find_ports += 1
                elif udp_protocol:
                    if result_udp == 0:
                        print(udp_full_text)
                        find_ports += 1
                else:
                    raise Exception

                sock_udp.close()
                sock_tcp.close()
            else:
                continue
    except Exception :
        print("You must select a protocol.")


if sys.argv[1] == "--help":
    help()


signal.signal(signal.SIGINT, handle_exit)

host = get_host_to_scan(shell_list)
tcp_protocol, udp_protocol = get_protocols_to_scan(shell_list)
start, end = get_ports_to_scan(shell_list)

connect_socket_to_ports(host, tcp_protocol, udp_protocol, start, end)

show_scanning_time()

