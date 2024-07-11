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
        server_message = self.client_socket.recv(8016).decode()
        if not server_message:
            return None
        print(server_message)
        return server_message

    def handle_input(self):

        self.receive_response()

        if self.role == 'Admin':
            self.handle_admin_input()
        elif self.role == 'Chef':
            self.handle_chef_input()
        elif self.role == 'Employee':
            self.handle_employee_input()

    def handle_admin_input(self):
        user_input = input("Enter Your Choice: ")
        self.send_command(user_input)
        if user_input == '1':  # Add Food Item
            item_name = input("Enter Food Item Name: ")
            item_price = input("Enter Food Item Price: ")
            item_category = input("Enter Food Item Category (as an integer): ")
            diet_type = input("Enter Food Item diet type ('Vegetarian', 'Non-Veg', 'Other'): ")
            spice_level = input("Enter Food Item spice level ('Low', 'Medium', 'High'): ")
            preference = input("Enter Food Item preference ('North Indian', 'South Indian', 'Other'): ")
            is_sweet = input("Enter Food Item is sweet or not(0/1): ")
            all_inputs = f"{item_name}|{item_price}|{item_category}|{diet_type}|{spice_level}|{preference}|{is_sweet}"
            self.send_command(all_inputs)
            self.receive_response()
        elif user_input == '2':  # Delete Food Item
            item_id = input("Enter Food Item Id to DELETE: ")
            self.send_command(item_id)
            self.receive_response()
        elif user_input == '3':  # Update Food Item
            item_id = input("Enter Food Item Id to UPDATE Availability Status: ")
            availability_status = input("Enter Availability Status: ")
            all_inputs = f"{item_id}|{availability_status}"
            self.send_command(all_inputs)
            self.receive_response()
        elif user_input == '4':
            print("Showing the menu items....")
            while self.receive_response() != "FoodItems ended":
                continue

    def handle_chef_input(self):
        user_input = input("Enter Your Choice: ")
        self.send_command(user_input)
        if user_input == '1':  # Check Voting Result
            print("Check Voting Result For the Food Items...")

        elif user_input == '2':  # View Feedback
            while self.receive_response() not in ["Discardable Ended", "No discardable items found."]:
                continue
            self.receive_response()
            action = input("Enter your choice: ")
            self.send_command(action)
            if action in ['1', '2']:
                item_id = input("Enter the Food Item ID: ")
                self.send_command(item_id)
            self.receive_response()

        elif user_input == '3':  # View Menu
            while self.receive_response() not in ["No Food Items Left", "No food items found."]:
                continue

        elif user_input == '4':  # View Recommendations
            while self.receive_response() not in ["Food Item Recommendations Ended", "No recommendations found."]:
                continue

    def handle_employee_input(self):
        user_input = input("Enter Your Choice: ")
        self.send_command(user_input)
        if user_input == '1':  # View Notifications
            while self.receive_response() not in ["Notifications Ended", "No new notifications."]:
                continue

        elif user_input == '2':  # Give Feedback
            food_item_id = input("Enter Food Item Id: ")
            rating = input("Enter Rating (1-5): ")
            feedback = input("Enter Feedback: ")
            all_inputs = f"{food_item_id}|{rating}|{feedback}"
            self.send_command(all_inputs)
            self.receive_response()

        elif user_input == '3':  # View Menu
            while self.receive_response() not in ["No Food Items Left", "No food items found."]:
                continue

        elif user_input == '4':
            while self.receive_response() not in ["Food Item Recommendations Ended", "No recommended items found."]:
                continue
            self.receive_response()
            food_item_id = input()
            self.send_command(food_item_id)
            self.receive_response()

        elif user_input == '5':
            while self.receive_response() not in ["Discarded Items Ended", "No Discard Items Found."]:
                continue

            food_item_id = input("Enter the food item id to discard: ")
            self.send_command(food_item_id)

            self.receive_response()
            disliked_aspects = input()
            self.send_command(disliked_aspects)

            self.receive_response()
            desired_taste = input()
            self.send_command(desired_taste)

            self.receive_response()
            mom_recipe = input()
            self.send_command(mom_recipe)

            #all_inputs = f"{disliked_aspects}|{desired_taste}|{mom_recipe}"
            #self.send_command(all_inputs)

    def start(self):
        self.connect()
        self.authenticate()

        #print("INSIDE START\n")
        self.handle_input()
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
