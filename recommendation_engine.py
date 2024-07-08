class RecommendationEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_top_10_recommendations(self):
        food_items = self.db_manager.getRecommendedItems()
        return food_items
