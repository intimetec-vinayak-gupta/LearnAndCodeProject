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
            self.handle_employee_command(user, command, client_socket)

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
            client_socket.send(f"Food item with Id '{item_id}' updated successfully, the IsAvailable changed to '{availability_status}'.\n".encode())

        elif command == '4':
            items = self.db_manager.view_food_items()
            if items:
                client_socket.send("Food Items:\n".encode())
                for item in items:
                    client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}\n".encode())
                    time.sleep(0.1)
            else:
                client_socket.send("No food items found.\n".encode())

        elif command == '5':
            client_socket.send("Exiting...\n".encode())
        else:
            client_socket.send("Invalid choice.\n".encode())

    def handle_chef_command(self, command, client_socket):
        # Implement chef command handling
        pass

    def handle_employee_command(self, user, command, client_socket):
        if command == '1':  # View Notifications
            # Implement viewing notifications
            pass
        elif command == '2':  # Give Feedback
            all_inputs = client_socket.recv(1024).decode().strip()
            food_item_id, rating, feedback = all_inputs.split('|')
            self.db_manager.add_rating_and_feedback(user.user_id, int(food_item_id), int(rating), feedback)
            client_socket.send(f"Feedback for food item '{food_item_id}' added successfully.\n".encode())
        elif command == '3':  # View Menu
            # Implement viewing menu
            pass
        elif command == '4':
            client_socket.send("Exiting...\n".encode())
        else:
            client_socket.send("Invalid choice.\n".encode())
