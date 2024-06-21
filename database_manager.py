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
            SELECT u.Name AS UserName, r.Name AS RoleName 
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
        query = "SELECT FoodItems.Id AS Id, FoodItems.Name AS Name, Price, IsAvailable, MealCategory.Name AS MealType FROM FoodItems JOIN MealCategory ON FoodItems.Category =  MealCategory.Id"
        return self.execute_query(query)
