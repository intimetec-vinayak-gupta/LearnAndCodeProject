import time
from recommendation_engine import RecommendationEngine


class CommandHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_command(self, user, command, client_socket):
        try:
            if user.role == "Admin":
                self.handle_admin_command(command, client_socket)
            elif user.role == "Chef":
                self.handle_chef_command(command, client_socket)
            elif user.role == "Employee":
                self.handle_employee_command(user, command, client_socket)
            else:
                client_socket.send("Invalid role.\n".encode())
        except Exception as e:
            client_socket.send(f"An error occurred: {e}\n".encode())

    def handle_admin_command(self, command, client_socket):
        try:
            if command == '1':
                self.add_food_item(client_socket)
            elif command == '2':
                self.delete_food_item(client_socket)
            elif command == '3':
                self.update_food_item(client_socket)
            elif command == '4':
                self.view_food_items(client_socket)
            elif command == '5':
                client_socket.send("Exiting...\n".encode())
            else:
                client_socket.send("Invalid choice.\n".encode())
        except Exception as e:
            client_socket.send(f"An error occurred: {e}\n".encode())

    def handle_chef_command(self, command, client_socket):
        try:
            if command == '1':
                self.view_voting_results(client_socket)
            elif command == '2':
                self.view_discardable_items(client_socket)
                self.handle_discard_or_delete(client_socket)
            elif command == '3':
                self.view_food_items(client_socket)
            elif command == '4':
                self.view_recommendations(client_socket)
            elif command == '5':
                client_socket.send("Exiting...\n".encode())
            else:
                client_socket.send("Invalid choice.\n".encode())
        except Exception as e:
            client_socket.send(f"An error occurred: {e}\n".encode())

    def handle_employee_command(self, user, command, client_socket):
        try:
            if command == '1':
                self.view_notifications(user, client_socket)
            elif command == '2':
                self.give_feedback(user, client_socket)
            elif command == '3':
                self.view_food_items(client_socket)
            elif command == '4':
                self.view_recommendations_and_choose(user, client_socket)
            elif command == '5':
                self.discard_item_procedure(client_socket)
            elif command == '6':
                client_socket.send("Exiting...\n".encode())
            else:
                client_socket.send("Invalid choice.\n".encode())
        except Exception as e:
            client_socket.send(f"An error occurred: {e}\n".encode())

    def add_food_item(self, client_socket):
        all_inputs = client_socket.recv(1024).decode().strip()
        self.db_manager.add_food_item(all_inputs)
        message = "Food item added successfully."
        self.db_manager.add_notification(message, int(1))
        client_socket.send(f"{message}\n".encode())

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
            for item in items:
                client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}, Price: {item['Price']}, Category: {item['Category']}".encode())
                time.sleep(0.1)
            client_socket.send("FoodItems ended".encode())
        else:
            client_socket.send("No food items found".encode())

    def view_voting_results(self, client_socket):
        items = self.db_manager.get_food_item_votes()
        if items:
            client_socket.send("Food Items:".encode())
            for item in items:
                client_socket.send(f"FoodItemId: {item['FoodItemId']}, Votes: {item['Votes']}".encode())
                time.sleep(0.1)
            client_socket.send("Voting List ended".encode())
        else:
            client_socket.send("No one has voted till now".encode())

    def handle_discard_or_delete(self, client_socket):
        client_socket.send("1. Add Item into Discarded List\n2. Delete the Item\n".encode())
        action = client_socket.recv(1024).decode().strip()

        if action == '1':
            food_item_id = client_socket.recv(1024).decode().strip()
            self.discard_item(food_item_id, client_socket)
            message = f"Food Item with Id: {food_item_id} has been discarded."
            self.db_manager.add_notification(message, 2)
        elif action == '2':
            food_item_id = client_socket.recv(1024).decode().strip()
            self.delete_food_item_by_id(food_item_id, client_socket)
        else:
            client_socket.send("Exiting discard/delete menu.\n".encode())

    def discard_item(self, food_item_id, client_socket):
        self.db_manager.discard_item(food_item_id)
        client_socket.send(f"Food item with Id '{food_item_id}' has been discarded successfully.\n".encode())

    def delete_food_item_by_id(self, food_item_id, client_socket):
        self.db_manager.delete_food_item(food_item_id)
        client_socket.send(f"Food item with Id '{food_item_id}' has been deleted successfully.\n".encode())

    def view_recommendations(self, client_socket):
        recommendations = self.get_recommendations()
        if recommendations:
            client_socket.send("Food Item Recommendations:".encode())
            for item in recommendations:
                client_socket.send(f"FoodItemId: {item['FoodItemId']}, FoodItemName: {item['FoodItemName']}, FoodItemCategory: {item['FoodItemCategory']}, AvgRating: {item['AvgRating']:.2f}, AvgSentiment: {item['AvgSentiment']:.2f}".encode())
                time.sleep(0.1)
            client_socket.send("Food Item Recommendations Ended".encode())
            message = "Food items are rolled out, choose the items you want to eat."
            self.db_manager.add_notification(message, 2)
        else:
            client_socket.send("No recommendations found".encode())

    def view_notifications(self, user, client_socket):
        last_seen_date = self.db_manager.get_last_seen_notification_date(user.user_id)
        new_notifications = self.db_manager.get_new_notifications(last_seen_date)
        if new_notifications:
            client_socket.send("New Notifications:\n".encode())
            for notification in new_notifications:
                client_socket.send(f"Date: {notification['Date']}, Message: {notification['Message']}".encode())
            client_socket.send("Notifications Ended".encode())
        else:
            client_socket.send("No new notifications".encode())

        self.db_manager.update_last_seen_notification_date(user.user_id)

    def give_feedback(self, user, client_socket):
        all_inputs = client_socket.recv(1024).decode().strip()
        food_item_id, rating, feedback = all_inputs.split('|')
        self.db_manager.add_rating_and_feedback(user.user_id, int(food_item_id), int(rating), feedback)
        client_socket.send(f"Feedback for food item '{food_item_id}' added successfully.\n".encode())

    def view_recommendations_and_choose(self, user, client_socket):
        recommended_items = self.db_manager.fetchRecommendedItemsBasedOnProfile(user.user_id)
        if recommended_items:
            client_socket.send("Food Item Recommendations:\n".encode())
            for item in recommended_items:
                client_socket.send(f"FoodItemId: {item['FoodItemId']}, FoodItemName: {item['FoodItemName']}, FoodItemCategory: {item['FoodItemCategory']}, AvgRating: {item['AvgRating']:.2f}, AvgSentiment: {item['AvgSentiment']:.2f}".encode())
                time.sleep(0.1)
            client_socket.send("Food Item Recommendations Ended".encode())
            client_socket.send("Enter the FoodItemId you want to choose:".encode())
            food_item_id = client_socket.recv(1024).decode().strip()
            self.choose_food_item(user, food_item_id, client_socket)
        else:
            client_socket.send("No recommended items found".encode())

    def choose_food_item(self, user, food_item_id, client_socket):
        if self.db_manager.is_food_item_recommended(int(food_item_id)):
            food_item_category = self.db_manager.get_food_item_category(int(food_item_id))
            if not self.db_manager.user_already_chosen_today(user.user_id, food_item_category):
                self.db_manager.insert_user_food_history(user.user_id, int(food_item_id), int(food_item_category))
                client_socket.send("Your choice has been recorded successfully.\n".encode())
            else:
                client_socket.send("You have already chosen a food item from this category today.\n".encode())
        else:
            client_socket.send("The food item is not in the recommendation, so you can't vote for this.\n".encode())

    def discard_item_procedure(self, client_socket):
        items = self.db_manager.view_discarded_items()
        if items:
            for item in items:
                client_socket.send(f"Id: {item['Id']}, FoodItemId: {item['FoodItemId']}\n".encode())
                time.sleep(0.1)
            client_socket.send("Discardable Items Ended".encode())
        else:
            client_socket.send("No Discard Items Found".encode())

        food_item_id = client_socket.recv(1024).decode().strip()
        if self.db_manager.is_discardable_item_exists(int(food_item_id)):
            self.collect_feedback_for_discarded_item(food_item_id, client_socket)
        else:
            client_socket.send("Discard item not found.\n".encode())

    def collect_feedback_for_discarded_item(self, food_item_id, client_socket):
        client_socket.send(f"What didn't you like about food item Id: {food_item_id}?\n".encode())
        answers1 = client_socket.recv(8016).decode().strip()

        client_socket.send(f"How would you like {food_item_id} to taste?\n".encode())
        answers2 = client_socket.recv(8016).decode().strip()

        client_socket.send("Share your mom's recipe\n".encode())
        answers3 = client_socket.recv(8016).decode().strip()

        print(answers1, answers2, answers3)

    def get_recommendations(self):
        recommendation_engine = RecommendationEngine(self.db_manager)
        return recommendation_engine.get_recommendations()

    def view_discardable_items(self, client_socket):
        items = self.db_manager.get_discardable_items()
        if items:
            client_socket.send("Discardable Items:\n".encode())
            for item in items:
                client_socket.send(f"Id: {item['Id']}, AvgRating: {item['AvgRating']}, AvgSentiment: {item['AvgSentiment']}\n".encode())
            client_socket.send("Discardable Items Ended".encode())
        else:
            client_socket.send("No discardable items found".encode())
