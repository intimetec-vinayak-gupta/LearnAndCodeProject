from database_manager import DatabaseManager as db

class NotificationDB:
        
    def add_notification(message, role):
        query = "INSERT INTO Notifications (Message, Role, Date) VALUES (%s, %s, NOW())"
        db.execute_query(query, (message, role))

    def get_last_seen_notification_date(user_id):
        query = "SELECT LastNotificationSeenDate FROM Users WHERE Id = %s"
        result = db.execute_query(query, (user_id,))
        return result[0]['LastNotificationSeenDate'] if result else None

    def get_new_notifications(last_seen_date):
        if last_seen_date:
            query = "SELECT * FROM Notifications WHERE Date > %s"
            return db.execute_query(query, (last_seen_date,))
        else:
            query = "SELECT * FROM Notifications"
            return db.execute_query(query)

    def update_last_seen_notification_date(user_id):
        query = "UPDATE Users SET LastNotificationSeenDate = NOW() WHERE Id = %s"
        db.execute_query(query, (user_id,))
