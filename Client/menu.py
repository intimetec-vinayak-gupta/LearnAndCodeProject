from client import Client

class Menu:
        
    def add_food_item():
        item_name = input("Enter Food Item Name: ")
        item_price = input("Enter Food Item Price: ")
        item_category = input("Enter Food Item Category (as an integer): ")
        diet_type = input("Enter Food Item diet type ('Vegetarian', 'Non-Veg', 'Other'): ")
        spice_level = input("Enter Food Item spice level ('Low', 'Medium', 'High'): ")
        preference = input("Enter Food Item preference ('North Indian', 'South Indian', 'Other'): ")
        is_sweet = input("Enter Food Item is sweet or not(0/1): ")
        all_inputs = f"{item_name}|{item_price}|{item_category}|{diet_type}|{spice_level}|{preference}|{is_sweet}"
        Client.send_command(all_inputs)
        Client.receive_response()

    def delete_food_item():
        item_id = input("Enter Food Item Id to DELETE: ")
        Client.send_command(item_id)
        Client.receive_response()

    def update_food_item():
        item_id = input("Enter Food Item Id to UPDATE Availability Status: ")
        availability_status = input("Enter Availability Status: ")
        all_inputs = f"{item_id}|{availability_status}"
        Client.send_command(all_inputs)
        Client.receive_response()

    def discard_item():
        while Client.receive_response() not in ["Discardable Ended", "No discardable items found."]:
            continue
        Client.receive_response()
        action = input("Enter your choice: ")
        Client.send_command(action)
        if action in ['1', '2']:
            item_id = input("Enter the Food Item ID: ")
            Client.send_command(item_id)
        Client.receive_response()

    def view_menu_item():
        while Client.receive_response() not in ["No Food Items Left", "No food items found."]:
            continue