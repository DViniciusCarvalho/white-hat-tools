import socket

def receber_arquivo(porta, arquivo):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', porta))
    s.listen(1)    
    while True:
        conn, addr = s.accept()
        with conn:
            tamanho_bytes = conn.recv(4)
            tamanho = int.from_bytes(tamanho_bytes, byteorder='big')
            conteudo = b''
            while len(conteudo) < tamanho:
                dados = conn.recv(tamanho - len(conteudo))
                if not dados:
                    break
                conteudo += dados
            with open(arquivo, 'wb') as f:
                f.write(conteudo)
            conn.close()
            break

porta = 50000
arquivo = 'info.txt'
receber_arquivo(porta, arquivo)