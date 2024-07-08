import mysql.connector

# MySQL database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'LearnAndCode_Project'
}

class DatabaseManager:
    def __init__(self, config=db_config):
        self.config = config

    def execute_query(self, query, params=None):
        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            if cursor.description:  # Check if there are results to fetch
                results = cursor.fetchall()
            else:
                results = []
            connection.commit()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    def get_user_role(self, username, password):
        query = """
            SELECT u.Id, u.Name AS UserName, r.Name AS RoleName 
            FROM Users u 
            JOIN Roles r ON u.RoleId = r.Id  
            JOIN UsersCredentials uc ON u.Id = uc.UserId 
            WHERE u.Name = %s AND uc.Password = %s
        """
        return self.execute_query(query, (username, password))

    def add_food_item(self, item_name, item_price, item_category):
        query = "INSERT INTO FoodItems (Name, Price, Category) VALUES (%s, %s, %s)"
        self.execute_query(query, (item_name, item_price, item_category))

    def delete_food_item(self, item_id):
        query = "DELETE FROM FoodItems WHERE Id = %s"
        self.execute_query(query, (item_id,))

    def update_food_item(self, item_id, availability_status):
        query = "UPDATE FoodItems SET IsAvailable = %s WHERE Id = %s"
        self.execute_query(query, (availability_status, item_id))

    def view_food_items(self):
        query = "SELECT * FROM FoodItems"
        return self.execute_query(query)

    def add_rating_and_feedback(self, user_id, food_item_id, rating, feedback):
        query = "INSERT INTO Ratings (UserId, FoodItemId, Rating, Feedback) VALUES (%s, %s, %s, %s);"
        # Execute the query with the parameters
        self.execute_query(query, (user_id, food_item_id, rating, feedback))

    def add_rating_and_feedback(self, user_id, food_item_id, rating, feedback):
        sentiment_score = self.calculate_sentiment(feedback)
        query = """
            INSERT INTO Ratings (UserId, FoodItemId, Rating, Feedback, SentimentScore) 
            VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_query(query, (user_id, food_item_id, rating, feedback, sentiment_score))

    def calculate_sentiment(self, feedback):
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

    def get_food_item_ratings(self, food_item_id):
        query = "SELECT Rating, SentimentScore FROM Ratings WHERE FoodItemId = %s"
        return self.execute_query(query, (food_item_id,))

    def truncate_recommended_items(self):
        query = "TRUNCATE TABLE RecommendedItemsDaily"
        self.execute_query(query)

    def fetchRecommendedItems(self):
        query = "SELECT FoodItemId, FoodItems.Name AS FoodItemName, FoodItemCategory, AvgRating, AvgSentiment FROM RecommendedItemsDaily JOIN FoodItems ON RecommendedItemsDaily.FoodItemId = FoodItems.Id;"
        return self.execute_query(query)

    def getRecommendedItems(self):
        self.truncate_recommended_items()
        query = """
                    INSERT INTO RecommendedItemsDaily (FoodItemId, FoodItemCategory, AvgRating, AvgSentiment)
                    SELECT FoodItemId, FoodItemCategory, AvgRating, AvgSentiment 
                    FROM (
                        SELECT 
                            FoodItemId,
                            MealCategory.Name AS FoodItemCategory,
                            AVG(Rating) AS AvgRating, 
                            AVG(SentimentScore) AS AvgSentiment, 
                            RANK() OVER (PARTITION BY MealCategory.Name ORDER BY AVG(Rating) DESC) AS ranks
                        FROM Ratings 
                        JOIN FoodItems ON Ratings.FoodItemId = FoodItems.Id
                        JOIN MealCategory ON FoodItems.Category = MealCategory.Id
                        GROUP BY FoodItemId, MealCategory.Name
                    ) AS result
                    WHERE ranks <= 3;
                """
        self.execute_query(query)
        return self.fetchRecommendedItems()

    def get_food_item_category(self, food_item_id):
        query = "SELECT Category FROM FoodItems WHERE FoodItems.Id = %s;"
        result = self.execute_query(query, (food_item_id,))
        return result[0]['Category'] if result else None

    def user_already_chosen_today(self, user_id, category):
        query = """
            SELECT 1 
            FROM UserFoodHistory ufh 
            JOIN FoodItems fi ON ufh.FoodItemId = fi.Id 
            WHERE ufh.UserId = %s AND fi.Category = %s AND DATE(ufh.DateTime) = CURDATE();
        """
        result = self.execute_query(query, (user_id, category))
        return len(result) > 0

    def get_daily_recommended_items(self):
        query = "SELECT * FROM RecommendedItemsDaily"
        return self.execute_query(query)

    def insert_user_food_history(self, user_id, food_item_id, food_item_category):
        query = "INSERT INTO UserFoodHistory (UserId, FoodItemId, FoodItemCategory, DateTime) VALUES (%s, %s, %s, NOW())"
        self.execute_query(query, (user_id, food_item_id, food_item_category))

    def is_food_item_recommended(self, food_item_id):
        query = "SELECT 1 FROM RecommendedItemsDaily WHERE FoodItemId = %s"
        result = self.execute_query(query, (food_item_id,))
        return len(result) > 0

    def add_notification(self, message, role):
        query = "INSERT INTO Notifications (Message, Role, Date) VALUES (%s, %s, NOW())"
        self.execute_query(query, (message, role))

    def get_last_seen_notification_date(self, user_id):
        query = "SELECT LastNotificationSeenDate FROM Users WHERE Id = %s"
        result = self.execute_query(query, (user_id,))
        return result[0]['LastNotificationSeenDate'] if result else None

    def get_new_notifications(self, last_seen_date, role):
        if last_seen_date:
            query = "SELECT * FROM Notifications WHERE Date > %s AND Role = %s"
            return self.execute_query(query, (last_seen_date, role))
        else:
            query = "SELECT * FROM Notifications WHERE Role = %s"
            return self.execute_query(query, (role,))

    def update_last_seen_notification_date(self, user_id):
        query = "UPDATE Users SET LastNotificationSeenDate = NOW() WHERE Id = %s"
        self.execute_query(query, (user_id,))