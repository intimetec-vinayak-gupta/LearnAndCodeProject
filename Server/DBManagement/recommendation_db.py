from database_manager import DatabaseManager as db
from menu_db import MenuDB


class RecommendationDB:
    def add_rating_and_feedback(self, user_id, food_item_id, rating, feedback):
        #update instance of calculate
        sentiment_score = self.calculate_sentiment(feedback)
        query = """
            INSERT INTO Ratings (UserId, FoodItemId, Rating, Feedback, SentimentScore) 
            VALUES (%s, %s, %s, %s, %s)
        """
        db.execute_query(query, (user_id, food_item_id, rating, feedback, sentiment_score))

    #TODO: move this fun to service
    def calculate_sentiment(feedback):
        positive_words = ["good", "great", "excellent", "fantastic", "amazing"]
        negative_words = ["bad", "terrible", "awful", "poor", "horrible"]

        score = 0
        words = feedback.lower().split()
        for word in words:
            if word in positive_words:
                score += 1
            elif word in negative_words:
                score -= 1

        # Normalize sentiment score to range 1-10
        max_score = len(words)
        normalized_score = ((score / max_score) + 1) * 5 if max_score != 0 else 5
        return max(1, min(10, normalized_score))

    def get_food_item_ratings(food_item_id):
        query = "SELECT Rating, SentimentScore FROM Ratings WHERE FoodItemId = %s"
        return db.execute_query(query, (food_item_id,))

    
    def getRecommendedItems(self):
        self.truncate_recommended_items()
        MenuDB.update_food_items_with_avg_scores()

        query = """
                    INSERT INTO RecommendedItemsDaily (FoodItemId, FoodItemCategory, AvgRating, AvgSentiment)
                    SELECT FoodItemId, FoodItemCategory, AvgRating, AvgSentiment 
                    FROM (
                        SELECT 
                            FoodItems.Id AS FoodItemId,
                            MealCategory.Name AS FoodItemCategory,
                            FoodItems.AvgRating AS AvgRating,
                            FoodItems.AvgSentiment AS AvgSentiment, 
                            ROW_NUMBER() OVER (PARTITION BY MealCategory.Name 
                            ORDER BY FoodItems.AvgSentiment DESC, FoodItems.AvgRating DESC) AS ranks
                        FROM FoodItems
                        JOIN MealCategory ON FoodItems.Category = MealCategory.Id
                        GROUP BY FoodItems.Id, MealCategory.Name
                    ) AS result
                    WHERE ranks <= 3;
                """
        db.execute_query(query)
        return self.fetchRecommendedItems()


    def truncate_recommended_items():
        query = "TRUNCATE TABLE RecommendedItemsDaily"
        db.execute_query(query)

    def fetchRecommendedItems():
        query = "SELECT FoodItemId, FoodItems.Name AS FoodItemName, FoodItemCategory, RecommendedItemsDaily.AvgRating, RecommendedItemsDaily.AvgSentiment FROM RecommendedItemsDaily JOIN FoodItems ON RecommendedItemsDaily.FoodItemId = FoodItems.Id;"
        return db.execute_query(query)

    
    def fetchRecommendedItemsBasedOnProfile(user_id):
        user_profile = db.fetchUserProfile(user_id)[0]
        diet_type = user_profile['diet_type']
        spice_level = user_profile['spice_level']
        preference = user_profile['preference']
        sweet_tooth = user_profile['sweet_tooth']
        
        query = """
                    SELECT r.FoodItemId, f.Name AS FoodItemName, r.FoodItemCategory, r.AvgRating, r.AvgSentiment
                    FROM RecommendedItemsDaily r
                    JOIN FoodItems f ON r.FoodItemId = f.Id
                    ORDER BY 
                        CASE WHEN f.DietType = %s THEN 1 ELSE 2 END, 
                        CASE WHEN f.Preference = %s THEN 1 ELSE 2 END, 
                        CASE WHEN f.SpiceLevel = %s THEN 1 ELSE 2 END, 
                        CASE WHEN f.IsSweet = %s THEN 1 ELSE 2 END;
                """
        return db.execute_query(query, (diet_type, spice_level, preference, sweet_tooth))




    def get_daily_recommended_items():
        query = "SELECT * FROM RecommendedItemsDaily"
        return db.execute_query(query)


    def is_food_item_recommended(food_item_id):
        query = "SELECT 1 FROM RecommendedItemsDaily WHERE FoodItemId = %s"
        result = db.execute_query(query, (food_item_id,))
        return len(result) > 0
