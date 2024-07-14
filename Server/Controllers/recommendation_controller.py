from ..DBManagement.recommendation_db import RecommendationDB
class RecommendationController:
    def get_recommendations(self):
        food_items = RecommendationDB.getRecommendedItems()
        return food_items
