from client import Client
class Recommendation:
    def get_recommendations():
        while Client.receive_response() not in ["Food Item Recommendations Ended", "No recommended items found."]:
            continue
        Client.receive_response()
        food_item_id = input()
        Client.send_command(food_item_id)
        Client.receive_response()
    
    def view_recommendations():
        while Client.receive_response() not in ["Food Item Recommendations Ended", "No recommendations found."]:
            continue
