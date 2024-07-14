from database_manager import DatabaseManager as db

class DiscardDB:
    
    def get_discardable_items():
        query = """
        SELECT Id, AvgRating, AvgSentiment 
        FROM FoodItems
        WHERE AvgRating <= 2.0 
          AND AvgSentiment <= 3.3 
          AND AvgRating != 0.0 
          AND AvgSentiment != 0.0
        """
        return db.execute_query(query)

    def discard_item(food_item_id):
        query = "INSERT INTO DiscardedItems (FoodItemId) VALUES (%s)"
        db.execute_query(query, (food_item_id,))


    def view_discarded_items():
        query = "SELECT Id, FoodItemId FROM DiscardedItems"
        return db.execute_query(query)

    def is_discardable_item_exists(food_item_id):
        query = "SELECT 1 FROM DiscardedItems WHERE FoodItemId = %s"
        return db.execute_query(query, (food_item_id,))