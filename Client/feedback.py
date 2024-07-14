from client import Client

class Feedback:
    
    def give_feedback():
        food_item_id = input("Enter Food Item Id: ")
        rating = input("Enter Rating (1-5): ")
        feedback = input("Enter Feedback: ")
        all_inputs = f"{food_item_id}|{rating}|{feedback}"
        Client.send_command(all_inputs)
        Client.receive_response()

    
    def get_discard_feedback():
        while Client.receive_response() not in ["Discarded Items Ended", "No Discard Items Found."]:
            continue

        food_item_id = input("Enter the food item id to discard: ")
        Client.send_command(food_item_id)

        Client.receive_response()
        disliked_aspects = input()
        Client.send_command(disliked_aspects)

        Client.receive_response()
        desired_taste = input()
        Client.send_command(desired_taste)

        Client.receive_response()
        mom_recipe = input()
        Client.send_command(mom_recipe)