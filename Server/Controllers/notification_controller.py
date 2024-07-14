from ..DBManagement.notification_db import NotificationDB
class NotificationController:
    def view_notifications(self, user, client_socket):
        last_seen_date = NotificationDB.get_last_seen_notification_date(user.user_id)
        print(last_seen_date)
        new_notifications = NotificationDB.get_new_notifications(last_seen_date)
        print("Notifications: ", new_notifications)
        if new_notifications:
            print("Notifications exists")
            client_socket.send("New Notifications:\n".encode())
            for notification in new_notifications:
                client_socket.send(f"Date: {notification['Date']}, Message: {notification['Message']}".encode())
            client_socket.send("Notifications Ended".encode())
        else:
            client_socket.send("No new notifications.".encode())

        NotificationDB.update_last_seen_notification_date(user.user_id)
