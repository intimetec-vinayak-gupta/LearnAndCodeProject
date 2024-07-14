from database_manager import DatabaseManager as db

class MenuDB:
    def add_food_item(item):
        item_name, item_price, item_category, diet_type, spice_level, preference, is_sweet = item.split('|')
        query = """
                    INSERT INTO FoodItems (Name, Price, Category, DietType, SpiceLevel, Preference, IsSweet)
                    VALUES(%s, %s, %s, %s, %s, %s, %s) 
                """
        db.execute_query(query, (item_name, float(item_price), int(item_category), diet_type, spice_level, preference, int(is_sweet)))

    def delete_food_item(item_id):
        query = "DELETE FROM FoodItems WHERE Id = %s"
        db.execute_query(query, (item_id,))

    def update_food_item(item_id, availability_status):
        query = "UPDATE FoodItems SET IsAvailable = %s WHERE Id = %s"
        db.execute_query(query, (availability_status, item_id))

    def view_food_items():
        query = "SELECT * FROM FoodItems"
        return db.execute_query(query)
    
    def update_food_items_with_avg_scores():
        query = """
        UPDATE FoodItems fi
        JOIN (
            SELECT 
                FoodItemId,
                AVG(Rating) AS AvgRating,
                AVG(SentimentScore) AS AvgSentiment
            FROM Ratings
            GROUP BY FoodItemId
        ) r ON fi.Id = r.FoodItemId
        SET 
            fi.AvgRating = r.AvgRating,
            fi.AvgSentiment = r.AvgSentiment
        """
        db.execute_query(query)

    
    def get_food_item_category(food_item_id):
        query = "SELECT Category FROM FoodItems WHERE FoodItems.Id = %s;"
        result = db.execute_query(query, (food_item_id,))
        return result[0]['Category'] if result else None
    
    
    def user_already_chosen_today(user_id, category):
        query = """
            SELECT 1 
            FROM UserFoodHistory ufh 
            JOIN FoodItems fi ON ufh.FoodItemId = fi.Id 
            WHERE ufh.UserId = %s AND fi.Category = %s AND DATE(ufh.DateTime) = CURDATE();
        """
        result = db.execute_query(query, (user_id, category))
        return len(result) > 0
    
    
    def get_food_item_votes():
        query = """
            SELECT fi.Id AS FoodItemId, COUNT(*) AS Votes
            FROM UserFoodHistory ufh 
            JOIN FoodItems fi ON ufh.FoodItemId = fi.Id
            GROUP BY fi.Id;
        """
        return db.execute_query(query)
    
    def insert_user_food_history(user_id, food_item_id, food_item_category):
        query = "INSERT INTO UserFoodHistory (UserId, FoodItemId, FoodItemCategory, DateTime) VALUES (%s, %s, %s, NOW())"
        db.execute_query(query, (user_id, food_item_id, food_item_category))
