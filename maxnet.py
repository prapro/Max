import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555  # Adjust this port to match the server's port
        self.addr = (self.server, self.port)
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
            return "Connected"
        except:
            return "Failed to connect"

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send_numbers(self, numbers):
        if self.connected:
            try:
                data = ' '.join(map(str, numbers))
                response = self.send(data)
                return response
            except socket.error as e:
                print(e)
        else:
            print("Not connected to the server.")

    def receive_numbers(self):
        if self.connected:
            try:
                response = self.client.recv(2048).decode()
                received_numbers = response.split()
                if len(received_numbers) == 4:
                    return [int(num) for num in received_numbers]
                else:
                    return None
            except socket.error as e:
                print(e)
        else:
            print("Not connected to the server.")

