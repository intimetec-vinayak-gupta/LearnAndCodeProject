from client import Client

class User:
    def __init__(self):
        self.role = None
        self.user_id = None

    def authenticate(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_credentials = f"{username}|{password}"
        Client.client_socket.send(user_credentials.encode())
        response = Client.receive_response()
        if "Login successful" in response:
            self.role = response.split("Your role is ")[1].strip().split('.')[0]
            self.user_id = response.split("Your user ID is ")[1].strip().split('.')[0]
    
    def handle_input(self):
        Client.receive_response()

        if self.role == 'Admin':
            self.handle_admin_input()
        elif self.role == 'Chef':
            self.handle_chef_input()
        elif self.role == 'Employee':
            self.handle_employee_input()

    def handle_admin_input(self):
        user_input = input("Enter Your Choice: ")
        Client.send_command(user_input)
        if user_input == '1':  # Add Food Item
            self.add_food_item()
        elif user_input == '2':  # Delete Food Item
            self.delete_food_item()
        elif user_input == '3':  # Update Food Item
            self.update_food_item()
        elif user_input == '4':
            self.view_menu_item()

    def handle_chef_input(self):
        user_input = input("Enter Your Choice: ")
        Client.send_command(user_input)
        if user_input == '1': 
            print("Check Voting Result For the Food Items...")
        elif user_input == '2':  
            self.discard_item()
        elif user_input == '3':  
            self.view_menu_item()
        elif user_input == '4':  
            self.view_recommendations()

    def handle_employee_input(self):
        user_input = input("Enter Your Choice: ")
        Client.send_command(user_input)
        if user_input == '1':  # View Notifications
            self.view_notifications()
        elif user_input == '2':  # Give Feedback
            self.give_feedback()
        elif user_input == '3':  # View Menu
            self.view_menu_item()
        elif user_input == '4':
            self.get_recommendations()
        elif user_input == '5':
            self.get_discard_feedback()
