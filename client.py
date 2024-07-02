import socket

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.role = None
        self.user_id = None

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
        self.client_socket.send(user_credentials.encode())
        response = self.receive_response()
        if "Login successful" in response:
            self.role = response.split("Your role is ")[1].strip().split('.')[0]
            self.user_id = response.split("Your user ID is ")[1].strip().split('.')[0]

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

            if self.role == 'Admin':
                self.handle_admin_input(user_input)
            elif self.role == 'Chef':
                self.handle_chef_input(user_input)
            elif self.role == 'Employee':
                self.handle_employee_input(user_input)

    def handle_admin_input(self, user_input):
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

    def handle_chef_input(self, user_input):
        # Implement Chef-specific input handling
        if user_input == '1':  # Finalize Menu
            print("Finalizing Menu...")
            # Additional logic to finalize the menu
        elif user_input == '2':  # View Feedback
            print("Viewing Feedback...")
            # Additional logic to view feedback
        elif user_input == '3':  # View Menu
            print("Viewing Menu...")
            # Additional logic to view the menu

    def handle_employee_input(self, user_input):
        if user_input == '1':  # View Notifications
            print("Viewing Notifications...")
            # Additional logic to view notifications
        elif user_input == '2':  # Give Feedback
            food_item_id = input("Enter Food Item Id: ")
            rating = input("Enter Rating (1-5): ")
            feedback = input("Enter Feedback: ")
            all_inputs = f"{food_item_id}|{rating}|{feedback}"
            self.send_command(all_inputs)
        elif user_input == '3':  # View Menu
            print("Viewing Menu...")
            # Additional logic to view the menu

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
    client = Client("127.0.0.1", 7777)
    client.start()
