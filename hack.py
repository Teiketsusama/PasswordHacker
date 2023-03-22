import socket
from sys import argv
from itertools import product


# try all possible combinations of upper and lower case for each letter for all words of the password dictionary
# passwords.txt contains all possible passwords


def password_combinations(password):
    for combination in product(*([c.upper(), c.lower()] for c in password)):
        yield "".join(combination)


def password_generator(filename):
    with open(filename, "r") as f:
        for line in f:
            yield from password_combinations(line.strip())


def try_pw():
    for password in password_generator("passwords.txt"):
        client_socket.send(password.encode())
        response = client_socket.recv(1024).decode()
        if response == "Connection success!":
            return password


with socket.socket() as client_socket:
    client_socket.connect((argv[1], int(argv[2])))

    print(try_pw())

