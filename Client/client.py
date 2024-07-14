import socket
from user import User

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            print(f"Connected to server at {self.server_address}:{self.server_port}")
        except socket.error as e:
            print(f"Connection error: {e}")


    def send_command(self, command):
        self.client_socket.send(command.encode())

    def receive_response(self):
        server_message = self.client_socket.recv(8016).decode()
        if not server_message:
            return None
        print(server_message)
        return server_message

    def start(self):
        self.connect()
        User.authenticate()

        #print("INSIDE START\n")
        User.handle_input()
        #while True:
         #   server_message = self.receive_response()
          #  if server_message is None:
           #     break
            #self.handle_input(server_message)

        self.client_socket.close()
        print("Disconnected from server")


if __name__ == "__main__":
    client = Client("127.0.0.1", 7778)
    client.start()
