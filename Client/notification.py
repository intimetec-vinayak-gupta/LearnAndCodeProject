from client import Client
class Notification:

    def view_notifications():
        while Client.receive_response() not in ["Notifications Ended", "No new notifications."]:
            continue