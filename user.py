class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

    def get_role_functions(self):
        role_functions = {
            "Admin": [
                "Login", "Add User", "Delete User", "Add Menu Item",
                "Update Menu Item", "Delete Menu Item", "View Menu"
            ],
            "Chef": [
                "Login", "Roll Out Tomorrow's Menu", "Finalize Menu",
                "Generate Monthly Report", "Update Availability of Menu Item",
                "View Feedback", "View Menu"
            ],
            "Employee": [
                "Login", "View Notifications", "Give Feedback",
                "Food Recommendation for Tomorrow", "View Feedback", "View Menu"
            ]
        }
        return role_functions.get(self.role, [])
