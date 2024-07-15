import socket
class User:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.role = None
        self.user_id = None

    def send_command(self, command):
        self.client_socket.send(command.encode())

    def receive_response(self):
        try:
            server_message = self.client_socket.recv(8016).decode()
            if not server_message:
                return None
            print(server_message)
            return server_message
        except socket.error as e:
            print(f"Socket error: {e}")
            return None

    def authenticate(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_credentials = f"{username}|{password}"
        self.send_command(user_credentials)
        
        response = self.receive_response()
        if response and "Login successful" in response:
            self.role = response.split("Your role is ")[1].strip().split('.')[0]
            self.user_id = response.split("Your user ID is ")[1].strip().split('.')[0]
            return True
        return False

    def handle_input(self):
        self.receive_response()
        if self.role == 'Admin':
            self.handle_admin_input()
        elif self.role == 'Chef':
            self.handle_chef_input()
        elif self.role == 'Employee':
            self.handle_employee_input()

    def handle_admin_input(self):
        while True:

            user_input = input("Enter Your Choice: ")
            self.send_command(user_input)
            if user_input == '1':  # Add Food Item
                self.add_food_item()
            elif user_input == '2':  # Delete Food Item
                self.delete_food_item()
            elif user_input == '3':  # Update Food Item
                self.update_food_item()
            elif user_input == '4':  # View Menu Item
                self.view_menu_item()
            else:
                print("Invalid choice. Please try again.")

    def handle_chef_input(self):
        while True:
            user_input = input("Enter Your Choice: ")
            self.send_command(user_input)
            if user_input == '1':  # Check Voting Result For the Food Items
                print("Check Voting Result For the Food Items...")
            elif user_input == '2':  # Discard Item
                self.discard_item()
            elif user_input == '3':  # View Menu Item
                self.view_menu_item()
            elif user_input == '4':  # View Recommendations
                self.view_recommendations()
            else:
                print("Invalid choice. Please try again.")

    def handle_employee_input(self):
        while True:
            user_input = input("Enter Your Choice: ")
            self.send_command(user_input)
            if user_input == '1':  # View Notifications
                self.view_notifications()
            elif user_input == '2':  # Give Feedback
                self.give_feedback()
            elif user_input == '3':  # View Menu
                self.view_menu_item()
            elif user_input == '4':  # Get Recommendations
                self.get_recommendations()
            elif user_input == '5':  # Get Discard Feedback
                self.get_discard_feedback()
            else:
                print("Invalid choice. Please try again.")

    def add_food_item(self):
        item = input("Enter the details of the food item: ")
        self.send_command(f"add_food_item|{item}")

    def delete_food_item(self):
        item_id = input("Enter the ID of the food item to delete: ")
        self.send_command(f"delete_food_item|{item_id}")

    def update_food_item(self):
        item_id = input("Enter the ID of the food item to update: ")
        availability_status = input("Enter the new availability status: ")
        self.send_command(f"update_food_item|{item_id}|{availability_status}")

    def view_menu_item(self):
        self.send_command("view_food_items")

    def discard_item(self):
        item_id = input("Enter the ID of the food item to discard: ")
        self.send_command(f"discard_item|{item_id}")

    def view_recommendations(self):
        self.send_command("view_recommendations")

    def view_notifications(self):
        self.send_command("view_notifications")

    def give_feedback(self):
        food_item_id = input("Enter the ID of the food item: ")
        rating = input("Enter your rating: ")
        feedback = input("Enter your feedback: ")
        self.send_command(f"add_rating_and_feedback|{food_item_id}|{rating}|{feedback}")

    def get_recommendations(self):
        self.send_command("get_recommendations")

    def get_discard_feedback(self):
        self.send_command("get_discard_feedback")
