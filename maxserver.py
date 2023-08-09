import socket
from _thread import *
import sys
from maxnet import Network  # Import the Network class from maxnet.py

server = "127.0.0.1"  # Change this to your server's IP address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_numbers(data):
    numbers = data.split()
    return [int(num) for num in numbers]

def make_numbers(numbers):
    return ' '.join(map(str, numbers))

numbers_set = [[0, 0, 0, 0], [100, 100, 100, 100]]

def threaded_client(conn, player, client_addr):
    if client_addr == "127.0.0.1":  # Check if the client is localhost
        conn.send(str.encode(make_numbers(numbers_set[player])))
        reply = ""
        while True:
            try:
                data = conn.recv(2048).decode()
                numbers = read_numbers(data)
                numbers_set[player] = numbers

                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = numbers_set[0]
                    else:
                        reply = numbers_set[1]

                    print("Received:", data)
                    print("Sending:", reply)

                conn.sendall(str.encode(make_numbers(reply)))
            except:
                break
    else:
        while True:
            try:
                data = conn.recv(2048).decode()
                numbers = read_numbers(data)
                numbers_set[player] = numbers

                if not data:
                    print("Disconnected")
                    break
                else:
                    print("Received:", data)
                    print("Setting numbers:", numbers)

            except:
                break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer, addr[0]))
    currentPlayer += 1

