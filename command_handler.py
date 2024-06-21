import time

class CommandHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_command(self, user, command, client_socket):
        if user.role == "Admin":
            self.handle_admin_command(command, client_socket)
        elif user.role == "Chef":
            self.handle_chef_command(command, client_socket)
        elif user.role == "Employee":
            print('Employee Handler ') #self.handle_employee_command(command, client_socket)
        else:
            client_socket.send("Invalid role.\n".encode())

    # Add more role handling if needed

    def handle_admin_command(self, command, client_socket):
        if command == '1':
            all_inputs = client_socket.recv(1024).decode().strip()
            item_name, item_price, item_category = all_inputs.split('|')
            self.db_manager.add_food_item(item_name, float(item_price), int(item_category))
            client_socket.send(f"Food item '{item_name}' added successfully.\n".encode())

        elif command == '2':
            item_id = int(client_socket.recv(1024).decode().strip())
            self.db_manager.delete_food_item(item_id)
            client_socket.send(f"Food item with Id '{item_id}' deleted successfully.\n".encode())

        elif command == '3':
            all_inputs = client_socket.recv(1024).decode().strip()
            item_id, availability_status = all_inputs.split('|')
            self.db_manager.update_food_item(int(item_id), int(availability_status))
            client_socket.send(
                f"Food item with Id '{item_id}' updated successfully, the IsAvailable changed to '{availability_status}'.\n".encode())

        elif command == '4':
            items = self.db_manager.view_food_items()
            if items:
                client_socket.send("Food Items:\n".encode())
                for item in items:
                    client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}, Price: {item['Price']}, IsAvailable: {item['IsAvailable']}, MealType: {item['MealType']},\n".encode())
                    time.sleep(0.1)
            else:
                client_socket.send("No food items found.\n".encode())

        elif command == '5':
            client_socket.send("Exiting...\n".encode())
        else:
            client_socket.send("Invalid choice.\n".encode())


    def handle_chef_command(self, command, client_socket):
        if command == '1':
            all_inputs = client_socket.recv(1024).decode().strip()
            item_name, item_price, item_category = all_inputs.split('|')
            self.db_manager.add_food_item(item_name, float(item_price), int(item_category))
            client_socket.send(f"Food item '{item_name}' added successfully.\n".encode())

        elif command == '2':
            client_socket.send("Exiting...\n".encode())
        else:
            client_socket.send("Invalid choice.\n".encode())


    def handle_employee_command(self, command, client_socket):
        pass