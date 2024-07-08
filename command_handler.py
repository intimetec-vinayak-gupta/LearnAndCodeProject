import time
from recommendation_engine import RecommendationEngine
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
            message = f"Food item '{item_name}' added successfully."
            self.db_manager.add_notification(str(message), int(1))
            client_socket.send(f"'{message}'\n".encode())
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
        if command == '1':  # Finalize Menu
            # Implement finalizing menu
            pass
        elif command == '2':  # View Feedback
            # Implement viewing feedback
            pass
        elif command == '3':  # View Menu
            items = self.db_manager.view_food_items()
            if items:
                client_socket.send("Food Items:\n".encode())
                for item in items:
                    client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}\n".encode())
                    time.sleep(0.1)
            else:
                client_socket.send("No food items found.\n".encode())
        elif command == '4':  # View Recommendations
            recommendations = self.get_recommendations()
            if recommendations:
                client_socket.send("Food Item Recommendations:\n".encode())
                for item in recommendations:
                    client_socket.send(f"FoodItemId: {item['FoodItemId']}, FoodItemName: {item['FoodItemName']},FoodItemCategory: {item['FoodItemCategory']}, AvgRating: {item['AvgRating']:.2f}, AvgSentiment: {item['AvgSentiment']:.2f}\n".encode())
                    time.sleep(0.1)
                message = f"Food items are rolled out, choose the items you wanted to eat."
                self.db_manager.add_notification(message, int(2))
            else:
                client_socket.send("No recommendations found.\n".encode())
        elif command == '5':
            client_socket.send("Exiting...\n".encode())
        else:
            client_socket.send("Invalid choice.\n".encode())


    def handle_employee_command(self, user, command, client_socket):
        if command == '1':  # View Notifications
            self.view_notifications(user, client_socket)
        elif command == '2':  # Give Feedback
            all_inputs = client_socket.recv(1024).decode().strip()
            food_item_id, rating, feedback = all_inputs.split('|')
            self.db_manager.add_rating_and_feedback(user.user_id, int(food_item_id), int(rating), feedback)
            client_socket.send(f"Feedback for food item '{food_item_id}' added successfully.\n".encode())
        elif command == '3':  # View Menu
            items = self.db_manager.view_food_items()
            if items:
                client_socket.send("Food Items:\n".encode())
                for item in items:
                    client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}\n".encode())
                    time.sleep(0.1)
            else:
                client_socket.send("No food items found.\n".encode())
        elif command == '4':
            recommended_items = self.db_manager.fetchRecommendedItems()
            print(recommended_items)

            if recommended_items:
                client_socket.send("Food Item Recommendations:\n".encode())
                for item in recommended_items:
                    client_socket.send(
                        f"FoodItemId: {item['FoodItemId']}, FoodItemName: {item['FoodItemName']},FoodItemCategory: {item['FoodItemCategory']}, AvgRating: {item['AvgRating']:.2f}, AvgSentiment: {item['AvgSentiment']:.2f}\n".encode())
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
                    client_socket.send(
                        "The food item is not in the recommendation, so you can't vote for this.\n".encode())
            else:
                client_socket.send("No recommended items found.\n".encode())
        elif command == '5':
            client_socket.send("Exiting...\n".encode())
        else:
            client_socket.send("Invalid choice.\n".encode())

    def view_notifications(self, user, client_socket):
        last_seen_date = self.db_manager.get_last_seen_notification_date(user.user_id)
        new_notifications = self.db_manager.get_new_notifications(last_seen_date, 2)

        if new_notifications:
            client_socket.send("New Notifications:\n".encode())
            for notification in new_notifications:
                client_socket.send(f"Date: {notification['Date']}, Message: {notification['Message']}\n".encode())
        else:
            client_socket.send("No new notifications.\n".encode())

        self.db_manager.update_last_seen_notification_date(user.user_id)

    def get_recommendations(self):
        recommendation_engine = RecommendationEngine(self.db_manager)
        return recommendation_engine.get_top_10_recommendations()