import requests
import signal
import sys
import time


shell_list = sys.argv
start_time = time.time()


def help():
    print("\n   DIRF [PROTOCOL://HOST] [WORDLIST(.TXT)] [-W] [-S]\n")
    print("        -w  Specifies that you are using a wordlist")
    print("        -s  Specifies that you want to see the tries\n")
    print("     Obs.: You must provide the host domain, not the IP. You must provide a wordlist and use the '-w' flag.\n")
    sys.exit()


def verify_help_command() -> None:
    try:
        if "--help" in shell_list:
            if len(shell_list) <= 2:
                help()
            raise ValueError
        return None
    except ValueError:
        print("Invalid command. Did you mean 'dirf --help'?")
        sys.exit()


def handle_ctrl_c(signal_received, frame):
    show_time()
    sys.exit


def show_time():
    end_time = time.time()
    total_time = end_time - start_time
    print("Process finished in: {:.3f}s".format(total_time))
    sys.exit()


def has_wordlist() -> None:
    try:
        for argument in shell_list:
            if ".txt" in argument:
                return None
        raise ValueError
    except ValueError:
        print("You must provide a wordlist with the correct path. See 'dirf --help'")
        sys.exit()


def host_has_protocol() -> None:
    try:
        for argument in shell_list:
            if "http://" in argument or "https://" in argument:
                return None
        raise ValueError
    except ValueError:
        print("The host must have protocol -> http/https. See 'dirf --help'")
        sys.exit()


def get_host() -> str:
    for argument in shell_list:
        if "http://" in argument or "https://" in argument:
            if argument[:-1] != "/":
                return argument + "/"
            return argument

def verify_host_disponibility(host: str) -> bool:
    try:
        requests.get(host)
    except requests.exceptions.RequestException:
        print("Host unavailable.")
        sys.exit()

def get_word_list() -> list[str]:
    for argument in shell_list:
        if ".txt" in argument:
            if "-w" in shell_list:
                return read_wordlist(argument).split("\n")
            print("You must use '-w' if you are using a wordlist. See 'dirf --help'")
            sys.exit()


def read_wordlist(file: str) -> str:
    try:
        with open(file) as wordlist:
            return wordlist.read()
    except FileNotFoundError:
        print("Wordlist not find.")
        sys.exit()
    

def show_command() -> bool:
    if "-s" in shell_list:
        return True
    return False


def find_directory(wordlist: list[str], host: str, show: bool):
    for directory in wordlist:
        full_url = f"{host}{directory}/"
        request = requests.get(full_url, auth=('user', 'pass'))
        if request.status_code == 200:           
            print(f"{full_url} -> 200 (OK)")
        elif request.status_code == 403:
            print(f"{full_url} -> 403 (Forbidden)") 
        elif request.status_code == 404 and show:
            print(f"{full_url} -> 404 (Not Found)")          
        continue
    show_time()


def main():
    signal.signal(signal.SIGINT, handle_ctrl_c)

    verify_help_command()
    host_has_protocol()
    has_wordlist()

    host = get_host()
    verify_host_disponibility(host)

    show = show_command()
    wordlist = get_word_list()

    find_directory(wordlist, host, show)
        

if __name__ == "__main__":
    main()