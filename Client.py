import socket

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

    def authenticate(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_credentials = f"{username}|{password}"
        print(user_credentials)
        self.client_socket.send(user_credentials.encode())

    def send_command(self, command):
        self.client_socket.send(command.encode())

    def receive_response(self):
        server_message = self.client_socket.recv(1024).decode()
        if not server_message:
            return None
        print(server_message)
        return server_message

    def handle_input(self, server_message):
        if "Enter" in server_message or "Press" in server_message:
            user_input = input()
            self.send_command(user_input)

            if user_input == '1':  # Add Food Item
                item_name = input("Enter Food Item Name: ")
                item_price = input("Enter Food Item Price: ")
                item_category = input("Enter Food Item Category (as an integer): ")
                all_inputs = f"{item_name}|{item_price}|{item_category}"
                self.send_command(all_inputs)
            elif user_input == '2':  # Delete Food Item
                item_id = input("Enter Food Item Id to DELETE: ")
                self.send_command(item_id)
            elif user_input == '3':  # Update Food Item
                item_id = input("Enter Food Item Id to UPDATE Availability Status: ")
                availability_status = input("Enter Availability Status: ")
                all_inputs = f"{item_id}|{availability_status}"
                self.send_command(all_inputs)

    def start(self):
        self.connect()
        self.authenticate()

        while True:
            server_message = self.receive_response()
            if server_message is None:
                break
            self.handle_input(server_message)

        self.client_socket.close()
        print("Disconnected from server")

if __name__ == "__main__":
    client = Client("127.0.0.1", 8889)
    client.start()
