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
    def __init__(self, config=db_config):
        self.config = config

    def execute_query(self, query, params=None):
        connection = None
        cursor = None
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
            print(f"Database Error: {err}")
            return []
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()