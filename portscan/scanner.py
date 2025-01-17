from bs4 import BeautifulSoup
from bs4 import ResultSet
from re import search
from typing import Tuple
import requests
import signal
import socket
import time
import sys


SHELL_LIST = sys.argv

FILENAME = sys.argv[0]

html_requested = requests.get("https://www.portalchapeco.com.br/jackson/portas.htm")
html_elements = BeautifulSoup(html_requested.content, "html.parser")

services_by_ports = []
find_ports = 0 

START_TIME = time.time()


def verify_help_command() -> None:
    if "--help" in SHELL_LIST:
        help()


def handle_exit(signal_received, frame) -> None:
    print("Scan finished with success.")
    show_scanning_time()   


def show_scanning_time() -> None:
    END_TIME = time.time()
    TOTAL_TIME =  END_TIME - START_TIME
    formatted_seconds = "{:.3f}s".format(TOTAL_TIME)

    print("Scan duration: ", formatted_seconds)
    print("Total ports find: ", find_ports)
    sys.exit()


def help() -> None:
    print("\n   Sintax: python3 -u FILENAME.py [HOST] [-t(DEFAULT)] [-u] [-i] [STARTPORT-ENDPORT] [-p] [PORT]\n")
    print("      -t    Allows TCP protocol")
    print("      -u    Allows UDP protocol")
    print("      -i    Especifies that the IPV4 address is not of a website\n")
    sys.exit()


def return_ports_interval_if_has(argument: str) -> bool | str:
    interval = search(r"[0-9]+[-][0-9]+", argument)
    if bool(interval):
        return str(argument)
    return False


def arguments_has_not_ip_specification(SHELL_LIST: list[str]) -> None:
    if not '-i' in SHELL_LIST:
        return True
    return False


def domain_name_has_not_protocol(argument: str) -> bool:
    if not ("http://" in argument) and not ("https://" in argument):
        return True
    return False


def current_argument_is_domain(argument: str) -> bool:
    ports_interval = return_ports_interval_if_has(argument)
    if bool(ports_interval):
        if argument != "-t" and argument != "-u" and argument != FILENAME and argument != ports_interval:
            return True
        return False
    elif argument != "-t" and argument != "-u" and argument != FILENAME:
        return True
    return False


def domain_has_http_protocol(host_domain: str) -> bool:
    if "http://" in host_domain:
        return True
    return False


def domain_has_https_protocol(host_domain: str) -> bool:
    if "https://" in host_domain:
        return True
    return False


def get_host_to_scan(SHELL_LIST: list[str]) -> str:
    try:
        for argument in SHELL_LIST:
            argument = str(argument)
            host_ip = search(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", argument)
            if bool(host_ip):
                if arguments_has_not_ip_specification(SHELL_LIST):
                    request_result_https = requests.get("https://" + argument)
                    request_result_http = requests.get("http://" + argument)
                    if request_result_https.status_code != 200:
                        if request_result_http.status_code != 200:
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
    

def get_ports_to_scan(SHELL_LIST: list[str]) -> Tuple[int, int]:
    for argument in SHELL_LIST:
        ports_interval = return_ports_interval_if_has(argument)
        if bool(ports_interval):
            interval_list = ports_interval.split("-")
            start_port = str(interval_list[0])
            end_port = str(interval_list[1])
            return int(start_port), int(end_port) + 1
        else:
            continue
    return 0, 1001


def tcp_is_selected(SHELL_LIST: list[str]) -> bool:
    try:
        list(SHELL_LIST).index("-t")
        return True
    except ValueError:
        if not udp_is_selected(SHELL_LIST):
            return True
        return False
    

def udp_is_selected(SHELL_LIST: list[str]) -> bool:
    try:
        list(SHELL_LIST).index("-u")
        return True
    except ValueError:
        return False


def get_protocols_to_scan(SHELL_LIST: list[str]) -> Tuple[bool, bool]:
    tcp_protocol = tcp_is_selected(SHELL_LIST)
    udp_protocol = udp_is_selected(SHELL_LIST)
    return tcp_protocol, udp_protocol


def port_is_documented(port_cell_elements: ResultSet) -> bool:
    number_of_port_cell = len(port_cell_elements)
    if number_of_port_cell:
        return True
    return False


def port_has_not_service(service_type: list[str]) -> bool:
    number_of_service = len(service_type)
    if number_of_service:
        return False
    return True


def organize_data_in_dict(port: int) -> bool:
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


def return_service_by_port(protocol: str) -> str:
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


def connect_socket_to_ports(host: str, tcp_protocol: bool, udp_protocol: bool, start: int, end: int) -> None:
    global find_ports
    try:
        for port in range(start, end):
            print(port)
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



signal.signal(signal.SIGINT, handle_exit)

verify_help_command()

host = get_host_to_scan(SHELL_LIST)
tcp_protocol, udp_protocol = get_protocols_to_scan(SHELL_LIST)
start, end = get_ports_to_scan(SHELL_LIST)

connect_socket_to_ports(host, tcp_protocol, udp_protocol, start, end)

show_scanning_time()