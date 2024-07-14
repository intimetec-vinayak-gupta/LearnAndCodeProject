import socket
import threading
from user import User
from Controllers.user_controller import UserController
from DBManagement.database_manager import DatabaseManager


class Server:
    def __init__(self, address, port, db_manager):
        self.address = address
        self.port = port
        self.db_manager = db_manager
        

    def handle_client(self, client_socket):
        try:
            print("Handling new client")
            user_credentials = client_socket.recv(1024).decode().strip()
            username, password = user_credentials.split('|')
            user_data = self.db_manager.get_user_role(username, password)

            if user_data:
                user = User(user_data[0]['Id'], username, user_data[0]['RoleName'])
                client_socket.send(f"Login successful! Your role is {user.role}. Your user ID is {user.user_id}.\n".encode())
                UserController.handle_command(user, client_socket)
            else:
                client_socket.send("Invalid credentials.\n".encode())
        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.address, self.port))
        server.listen(5)
        print(f"Server started on port {self.port}")
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    db_manager = DatabaseManager()
    server = Server("0.0.0.0", 7779, db_manager)
    server.start()
