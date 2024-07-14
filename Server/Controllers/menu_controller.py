from ..DBManagement.discard_db import DiscardDB
from ..DBManagement.menu_db import MenuDB
class MenuController:  
    
    def view_discardable_items(self, client_socket):
        items = DiscardDB.get_discardable_items()
        if items:
            client_socket.send("Discardable Items:\n".encode())
            for item in items:
                client_socket.send(
                    f"Id: {item['Id']}, AvgRating: {item['AvgRating']}, AvgSentiment: {item['AvgSentiment']}\n".encode())
            client_socket.send("Discardable Ended".encode())
        else:
            client_socket.send("No discardable items found.".encode())

    def discard_item(self, food_item_id, client_socket):
        DiscardDB.discard_item(food_item_id)
        client_socket.send(f"Food item with Id '{food_item_id}' has been discarded successfully.\n".encode())

    def delete_food_item(self, food_item_id, client_socket):
        MenuDB.delete_food_item(food_item_id)
        client_socket.send(f"Food item with Id '{food_item_id}' has been deleted successfully.\n".encode())