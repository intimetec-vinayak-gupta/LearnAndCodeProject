import socket
from user import User

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user = User(self.client_socket)  # Pass the socket to User instance

    def connect(self):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            print(f"Connected to server at {self.server_address}:{self.server_port}")
        except socket.error as e:
            print(f"Connection error: {e}")
            self.client_socket.close()
            return False
        return True

    def start(self):
        if not self.connect():
            return
        
        if not self.user.authenticate():
            print("Authentication failed")
            self.client_socket.close()
            return
        
        self.user.handle_input()
        
        self.client_socket.close()
        print("Disconnected from server")

if __name__ == "__main__":
    client = Client("127.0.0.1", 7779)
    client.start()
