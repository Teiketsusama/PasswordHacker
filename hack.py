import socket
import sys
import itertools
import string


def try_pw():
    for i in range(1000000):
        passwords = itertools.product(string.ascii_lowercase + string.digits, repeat=i + 1)
        for password in passwords:
            client_socket.send(bytes(''.join(password), 'utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            if response == 'Connection success!':
                print(''.join(password))
                client_socket.close()
                return


with socket.socket() as client_socket:
    client_socket.connect((sys.argv[1], int(sys.argv[2])))

    try_pw()
