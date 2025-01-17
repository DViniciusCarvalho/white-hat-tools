import os
import requests
import signal
import sys
import time
from typing import Tuple


shell_list = sys.argv

start_time = None
stopped = False


def show_time():
    end_time = time.time()
    total_time = end_time - start_time   
    print("Process finished in: {:.3f}s".format(total_time))  
    sys.exit()


def handle_exit(signal_received, frame):
    global stopped
    if signal_received == signal.SIGINT:
        stopped = True


def analyse_help_argument() -> None:
    if "--help" in shell_list:
        if len(shell_list) == 2:
            help()
        else:
            print("Command not valid.")
            sys.exit()


def help() -> None:
    print("   SUBF [PROTOCOL://HOST] [WORDLIST(.TXT)] [-w] [-s]\n")
    print("     -w   Define that a wordlist is being used")
    print("     -s   Allow the script to show all the subdomains tested\n")
    print("   OBS.: IF YOU ARE USING A WORDLIST, YOU MUST USE '-w'. IN THE WORDLIST, THE SUBDOMAINS MUST BE SEPARATED BY BREAK LINES")
    sys.exit()


def verify_if_host_has_protocol() -> None:
    host_http = any("http://" in argument for argument in shell_list)
    host_https = any("https://" in argument for argument in shell_list)
    if host_http or host_https:
        return None
    print("The host must have a protocol: HTTP or HTTPS")
    sys.exit()


def verify_if_has_wordlist() -> None:
    wordlist = any(".txt" in argument for argument in shell_list)
    wordlist_command = "-w" in shell_list
    if wordlist:
        if wordlist_command:
            return None
        print("Must have the '-w' command if you are using your own wordlist.")
        sys.exit()
    print("You must select a wordlist.")
    sys.exit()


def verify_show_command() -> bool:
    if "-s" in shell_list:
        return True
    return False


def get_host_and_protocol() -> Tuple[str, str]:
    for argument in shell_list:
        if "http://" in argument:
            verify_host_disponibility(argument)
            protocol = argument[:7]
            host = argument[7:]
            return (protocol, host)
        elif "https://" in argument:
            verify_host_disponibility(argument)
            protocol = argument[:8]
            host = argument[8:]
            return (protocol, host)
        continue


def verify_host_disponibility(host: str) -> None:
    try:
        requests.get(host)
        return None
    except requests.exceptions.RequestException:
        print("Host not available.")
        sys.exit()

def get_wordlist() -> list[str]:
    current_directory = os.path.abspath(os.getcwd())
    for argument in shell_list:
        if ".txt" in argument:
            full_path = current_directory + "/" + argument
            return read_wordlist(full_path)
 

def read_wordlist(full_path: str) -> list[str]:
    try:
        with open(full_path, "r") as file:
            content = file.read()
            subdomain_list = content.split("\n")
            return subdomain_list
    except FileNotFoundError:
        print("File not found. Verify if it is in the same directory that you are")
        sys.exit()


def do_subdomain_request(protocol: str, host: str, subdomains: list[str], show: bool) -> None:
    global start_time
    start_time = time.time()
    for subdomain in subdomains:
        if not stopped:
            full_url = protocol + subdomain + "." + host
            try:
                request = requests.get(full_url, auth=("user", "pass"))
                if request.status_code == 200:
                    print(f"{full_url} -> 200 (OK)")
                elif request.status_code == 403:
                    print(f"{full_url} -> 403 (FORBIDDEN)")
            except requests.exceptions.RequestException:
                if show:
                    print(f"{full_url} -> 404 (NOT FOUND)")
                continue
        else:
            show_time()
            return None


signal.signal(signal.SIGINT, handle_exit)

analyse_help_argument()
verify_if_host_has_protocol()
verify_if_has_wordlist()

show_command = verify_show_command()
protocol, host = get_host_and_protocol()
subdomain_list = get_wordlist()

do_subdomain_request(protocol, host, subdomain_list, show_command)