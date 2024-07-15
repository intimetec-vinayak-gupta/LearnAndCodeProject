import mysql.connector
from datetime import datetime
# MySQL database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'LearnAndCode_Project'
}


class DatabaseManager:
    def __init__(self, config = db_config):
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

    def add_food_item(self, item):
        item_name, item_price, item_category, diet_type, spice_level, preference, is_sweet = item.split('|')
        query = """
                    INSERT INTO FoodItems (Name, Price, Category, DietType, SpiceLevel, Preference, IsSweet)
                    VALUES(%s, %s, %s, %s, %s, %s, %s) 
                """
        self.execute_query(query, (item_name, float(item_price), int(item_category), diet_type, spice_level, preference, int(is_sweet)))

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
        sentiment_score = self.calculate_sentiment(feedback)
        query = """
            INSERT INTO Ratings (UserId, FoodItemId, Rating, Feedback, SentimentScore) 
            VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_query(query, (user_id, food_item_id, rating, feedback, sentiment_score))

    def calculate_sentiment(self, feedback):
        positive_words = [
            "good", "great", "excellent", "fantastic", "amazing", "wonderful", "superb", "positive", "pleasant", "nice",
            "awesome", "outstanding", "brilliant", "exceptional", "fabulous", "marvelous", "satisfying", "delightful",
            "impressive", "commendable", "splendid", "terrific", "lovely", "enjoyable", "cool"]

        negative_words = [
            "bad", "terrible", "awful", "poor", "horrible", "dreadful", "unpleasant", "negative", "disappointing",
            "subpar", "lousy", "unacceptable", "inferior", "crummy", "atrocious", "appalling", "pathetic", "abysmal",
            "unfavorable", "nasty", "deficient", "deplorable", "horrid", "mediocre", "unimpressive"]

        negations = ["not", "never", "no", "none", "cannot", "can't", "won't", "don't", "doesn't", "didn't", "isn't",
                     "aren't", "wasn't", "weren't"]

        score = 0
        words = feedback.lower().split()
        i = 0
        while i < len(words):
            word = words[i]
            if word in positive_words:
                if i > 0 and words[i - 1] in negations:
                    score -= 1
                else:
                    score += 1
            elif word in negative_words:
                if i > 0 and words[i - 1] in negations:
                    score += 1
                else:
                    score -= 1
            i += 1

            # Consider pairs of words (like "not good")
            if i < len(words) - 1:
                bigram = f"{words[i]} {words[i + 1]}"
                if bigram in positive_words:
                    if i > 1 and words[i - 1] in negations:
                        score -= 1
                    else:
                        score += 1
                    i += 1
                elif bigram in negative_words:
                    if i > 1 and words[i - 1] in negations:
                        score += 1
                    else:
                        score -= 1
                    i += 1

        # Normalize sentiment score to range 1-10
        max_score = len(words)
        normalized_score = ((score / max_score) + 1) * 5 if max_score != 0 else 5
        return max(1, min(10, normalized_score))

    def get_food_item_ratings(self, food_item_id):
        query = "SELECT Rating, SentimentScore FROM Ratings WHERE FoodItemId = %s"
        return self.execute_query(query, (food_item_id,))

    def update_food_items_with_avg_scores(self):
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
        self.execute_query(query)

    def get_recommended_items(self):
        self.truncate_recommended_items()
        self.update_food_items_with_avg_scores()

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
        self.execute_query(query)
        return self.fetchRecommendedItems()

    def get_food_item_category(self, food_item_id):
        query = "SELECT Category FROM FoodItems WHERE FoodItems.Id = %s;"
        result = self.execute_query(query, (food_item_id,))
        return result[0]['Category'] if result else None

    def truncate_recommended_items(self):
        query = "TRUNCATE TABLE RecommendedItemsDaily"
        self.execute_query(query)

    def fetchRecommendedItems(self):
        query = "SELECT FoodItemId, FoodItems.Name AS FoodItemName, FoodItemCategory, RecommendedItemsDaily.AvgRating, RecommendedItemsDaily.AvgSentiment FROM RecommendedItemsDaily JOIN FoodItems ON RecommendedItemsDaily.FoodItemId = FoodItems.Id;"
        return self.execute_query(query)

    def fetchUserProfile(self, user_id):
        query = "SELECT diet_type, spice_level, preference, sweet_tooth FROM Userprofile WHERE user_id = %s;"
        return self.execute_query(query, (user_id,))

    def fetchRecommendedItemsBasedOnProfile(self, user_id):
        user_profile = self.fetchUserProfile(user_id)[0]
        diet_type = user_profile['diet_type']
        spice_level = user_profile['spice_level']
        preference = user_profile['preference']
        sweet_tooth = user_profile['sweet_tooth']
        print(user_profile)
        print(diet_type, spice_level, preference, sweet_tooth)
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
        return self.execute_query(query, (diet_type, spice_level, preference, sweet_tooth))

    def user_already_chosen_today(self, user_id, category):
        query = """
            SELECT 1 
            FROM UserFoodHistory ufh 
            JOIN FoodItems fi ON ufh.FoodItemId = fi.Id 
            WHERE ufh.UserId = %s AND fi.Category = %s AND DATE(ufh.DateTime) = CURDATE();
        """
        result = self.execute_query(query, (user_id, category))
        return len(result) > 0

    def get_food_item_votes(self):
        query = """
            SELECT fi.Id AS FoodItemId, COUNT(*) AS Votes
            FROM UserFoodHistory ufh 
            JOIN FoodItems fi ON ufh.FoodItemId = fi.Id
            GROUP BY fi.Id;
        """
        return self.execute_query(query)

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

    def get_new_notifications(self, last_seen_date):
        if last_seen_date:
            query = "SELECT * FROM Notifications WHERE Date > %s"
            return self.execute_query(query, (last_seen_date,))
        else:
            query = "SELECT * FROM Notifications"
            return self.execute_query(query)

    def update_last_seen_notification_date(self, user_id):
        query = "UPDATE Users SET LastNotificationSeenDate = NOW() WHERE Id = %s"
        self.execute_query(query, (user_id,))

    def get_discardable_items(self):
        query = """
        SELECT Id, AvgRating, AvgSentiment 
        FROM FoodItems
        WHERE AvgRating <= 2.0 
          AND AvgSentiment <= 3.3 
          AND AvgRating != 0.0 
          AND AvgSentiment != 0.0
        """
        return self.execute_query(query)

    def discard_item(self, food_item_id):
        query = "INSERT INTO DiscardedItems (FoodItemId) VALUES (%s)"
        self.execute_query(query, (food_item_id,))

    def view_discarded_items(self):
        query = "SELECT Id, FoodItemId FROM DiscardedItems"
        return self.execute_query(query)

    def is_discardable_item_exists(self, food_item_id):
        query = "SELECT 1 FROM DiscardedItems WHERE FoodItemId = %s"
        return self.execute_query(query, (food_item_id,))