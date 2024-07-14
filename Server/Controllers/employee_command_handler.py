import time

class EmployeeCommandHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_command(self, user, command, client_socket):
        if command == '1':
            self.view_notifications(user, client_socket)
        elif command == '2':
            self.give_feedback(user, client_socket)
        elif command == '3':
            self.view_menu(client_socket)
        elif command == '4':
            self.view_recommended_items(user, client_socket)
        elif command == '5':
            self.view_discarded_items(client_socket)
        elif command == '6':
            self.exit(client_socket)
        else:
            self.invalid_choice(client_socket)

    def view_notifications(self, user, client_socket):
        notifications = self.db_manager.get_notifications(user.user_id)
        if notifications:
            client_socket.send("Notifications:\n".encode())
            for notification in notifications:
                client_socket.send(f"Notification: {notification['message']}\n".encode())
                time.sleep(0.1)
        else:
            client_socket.send("No notifications found.\n".encode())

    def give_feedback(self, user, client_socket):
        all_inputs = client_socket.recv(1024).decode().strip()
        food_item_id, rating, feedback = all_inputs.split('|')
        self.db_manager.add_rating_and_feedback(user.user_id, int(food_item_id), int(rating), feedback)
        client_socket.send(f"Feedback for food item '{food_item_id}' added successfully.\n".encode())

    def view_menu(self, client_socket):
        items = self.db_manager.view_food_items()
        if items:
            client_socket.send("Food Items:\n".encode())
            for item in items:
                client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}\n".encode())
                time.sleep(0.1)
        else:
            client_socket.send("No food items found.\n".encode())

    def view_recommended_items(self, user, client_socket):
        recommended_items = self.db_manager.fetchRecommendedItemsBasedOnProfile(user.user_id)
        if recommended_items:
            client_socket.send("Food Item Recommendations:\n".encode())
            for item in recommended_items:
                client_socket.send(f"FoodItemId: {item['FoodItemId']}, FoodItemName: {item['FoodItemName']}, FoodItemCategory: {item['FoodItemCategory']}, AvgRating: {item['AvgRating']:.2f}, AvgSentiment: {item['AvgSentiment']:.2f}\n".encode())
                time.sleep(0.1)
            client_socket.send("Enter the FoodItemId you want to choose:\n".encode())
            food_item_id = client_socket.recv(1024).decode().strip()
            if self.db_manager.is_food_item_recommended(int(food_item_id)):
                food_item_category = self.db_manager.get_food_item_category(int(food_item_id))
                if not self.db_manager.user_already_chosen_today(user.user_id, food_item_category):
                    self.db_manager.insert_user_food_history(user.user_id, int(food_item_id), int(food_item_category))
                    client_socket.send("Your choice has been recorded successfully.\n".encode())
                else:
                    client_socket.send("You have already chosen a food item from this category today.\n".encode())
            else:
                client_socket.send("The food item is not in the recommendation, so you can't vote for this.\n".encode())
        else:
            client_socket.send("No recommended items found.\n".encode())

    def view_discarded_items(self, client_socket):
        items = self.db_manager.view_discarded_items()
        if items:
            client_socket.send("Discarded Items:\n".encode())
            for item in items:
                client_socket.send(f"Id: {item['Id']}, FoodItemId: {item['FoodItemId']}\n".encode())
                time.sleep(0.1)
        else:
            client_socket.send("No discard items found.\n".encode())

        food_item_id = client_socket.recv(1024).decode().strip()
        if self.db_manager.is_discardable_item_exists(int(food_item_id)):
            client_socket.send(f"What didn't you like about food item Id: {food_item_id}?\n".encode())
            answers1 = client_socket.recv(8016).decode().strip()
            client_socket.send(f"How would you like {food_item_id} to taste?\n".encode())
            answers2 = client_socket.recv(8016).decode().strip()
            client_socket.send("Share your mom's recipe\n".encode())
            answers3 = client_socket.recv(8016).decode().strip()
            print(answers1, "   ", answers2, "   ", answers3)

    def exit(self, client_socket):
        client_socket.send("Exiting...\n".encode())

    def invalid_choice(self, client_socket):
        client_socket.send("Invalid choice.\n".encode())
