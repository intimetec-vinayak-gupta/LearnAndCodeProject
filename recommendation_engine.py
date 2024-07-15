class RecommendationEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_recommendations(self):
        try:
            food_items = self.db_manager.get_recommended_items()
            return food_items
        except Exception as e:
            print(f"Error while getting recommendations: {e}")
            return []