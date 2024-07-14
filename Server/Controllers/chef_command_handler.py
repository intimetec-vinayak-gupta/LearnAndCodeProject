import time

class ChefCommandHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_command(self, command, client_socket):
        if command == '1':
            self.check_voting_result(client_socket)
        elif command == '2':
            self.view_discardable_items(client_socket)
        elif command == '3':
            self.view_menu(client_socket)
        elif command == '4':
            self.view_recommendations(client_socket)
        elif command == '':
            self.exit(client_socket)
        else:
            self.invalid_choice(client_socket)

    def check_voting_result(self, client_socket):
        items = self.db_manager.get_food_item_votes()
        if items:
            client_socket.send("Food Items:\n".encode())
            for item in items:
                client_socket.send(f"FoodItemId: {item['FoodItemId']}, Votes: {item['Votes']}\n".encode())
                time.sleep(0.1)
        else:
            client_socket.send("No one has voted till now.\n".encode())

    def view_discardable_items(self, client_socket):
        items = self.db_manager.view_discardable_items()
        if items:
            client_socket.send("Discardable Food Items:\n".encode())
            for item in items:
                client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}, Price: {item['Price']}, Category: {item['Category']}\n".encode())
                time.sleep(0.1)
            client_socket.send("1. Add Item into Discarded List\n2. Delete the Item\n".encode())
            action = client_socket.recv(1024).decode().strip()
            if action == '1':
                food_item_id = client_socket.recv(1024).decode().strip()
                self.discard_item(food_item_id, client_socket)
                message = f"Food Item with Id: {food_item_id} has been discarded."
                self.db_manager.add_notification(message, 2)
            elif action == '2':
                food_item_id = client_socket.recv(1024).decode().strip()
                self.delete_food_item(food_item_id, client_socket)
            else:
                client_socket.send("Exiting discard/delete menu.\n".encode())
        else:
            client_socket.send("No discardable food items found.\n".encode())

    def view_menu(self, client_socket):
        items = self.db_manager.view_food_items()
        if items:
            client_socket.send("Food Items:\n".encode())
            for item in items:
                client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}, Price: {item['Price']}, Category: {item['Category']}\n".encode())
                time.sleep(0.1)
        else:
            client_socket.send("No food items found.\n".encode())

    def view_recommendations(self, client_socket):
        recommendations = self.db_manager.get_recommendations()
        if recommendations:
            client_socket.send("Food Item Recommendations:\n".encode())
            for item in recommendations:
                client_socket.send(f"FoodItemId: {item['FoodItemId']}, FoodItemName: {item['FoodItemName']}, FoodItemCategory: {item['FoodItemCategory']}, AvgRating: {item['AvgRating']:.2f}, AvgSentiment: {item['AvgSentiment']:.2f}\n".encode())
                time.sleep(0.1)
        else:
            client_socket.send("No recommendations found.\n".encode())

    def discard_item(self, food_item_id, client_socket):
        self.db_manager.discard_food_item(food_item_id)
        client_socket.send(f"Food item with Id '{food_item_id}' discarded successfully.\n".encode())

    def delete_food_item(self, food_item_id, client_socket):
        self.db_manager.delete_food_item(food_item_id)
        client_socket.send(f"Food item with Id '{food_item_id}' deleted successfully.\n".encode())

    def exit(self, client_socket):
        client_socket.send("Exiting...\n".encode())

    def invalid_choice(self, client_socket):
        client_socket.send("Invalid choice.\n".encode())
