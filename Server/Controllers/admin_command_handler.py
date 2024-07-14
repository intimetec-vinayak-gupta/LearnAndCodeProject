import time

class AdminCommandHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_command(self, command, client_socket):
        if command == '1':
            self.add_food_item(client_socket)
        elif command == '2':
            self.delete_food_item(client_socket)
        elif command == '3':
            self.update_food_item(client_socket)
        elif command == '4':
            self.view_food_items(client_socket)
        elif command == '5':
            self.exit(client_socket)
        else:
            self.invalid_choice(client_socket)

    def add_food_item(self, client_socket):
        all_inputs = client_socket.recv(1024).decode().strip()
        self.db_manager.add_food_item(all_inputs)
        message = f"Food item added successfully."
        self.db_manager.add_notification(message, 1)
        client_socket.send(f"'{message}'\n".encode())

    def delete_food_item(self, client_socket):
        item_id = int(client_socket.recv(1024).decode().strip())
        self.db_manager.delete_food_item(item_id)
        client_socket.send(f"Food item with Id '{item_id}' deleted successfully.\n".encode())

    def update_food_item(self, client_socket):
        all_inputs = client_socket.recv(1024).decode().strip()
        item_id, availability_status = all_inputs.split('|')
        self.db_manager.update_food_item(int(item_id), int(availability_status))
        client_socket.send(f"Food item with Id '{item_id}' updated successfully, the IsAvailable changed to '{availability_status}'.\n".encode())

    def view_food_items(self, client_socket):
        items = self.db_manager.view_food_items()
        if items:
            client_socket.send("Food Items:\n".encode())
            for item in items:
                client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}, Price: {item['Price']}, Category: {item['Category']}\n".encode())
                time.sleep(0.1)
        else:
            client_socket.send("No food items found.\n".encode())

    def exit(self, client_socket):
        client_socket.send("Exiting...\n".encode())

    def invalid_choice(self, client_socket):
        client_socket.send("Invalid choice.\n".encode())
