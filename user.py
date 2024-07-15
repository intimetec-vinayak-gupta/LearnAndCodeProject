class UserError(Exception):
    pass


class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

    def get_role_functions(self):
        try:
            role_functions = {
                "Admin": ["add_food_item", "delete_food_item", "update_food_item", "view_food_items"],
                "Chef": ["add_food_item", "update_food_item", "view_food_items"],
                "Employee": ["view_food_items", "add_rating_and_feedback"],
            }
            return role_functions.get(self.role, [])
        except Exception as e:
            print(f"Error getting role functions: {e}")
            raise UserError(f"Error getting role functions: {e}")
