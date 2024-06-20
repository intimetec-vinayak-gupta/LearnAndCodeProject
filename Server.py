import socket
import threading
from database_manager import DatabaseManager
from user import User
from command_handler import CommandHandler

class Server:
    def __init__(self, address, port, db_manager, command_handler):
        self.address = address
        self.port = port
        self.db_manager = db_manager
        self.command_handler = command_handler

    def handle_client(self, client_socket):
        try:
            print("Handling new client")
            user_credentials = client_socket.recv(1024).decode().strip()
            print(user_credentials)
            username, password = user_credentials.split('|')
            print(f"Received credentials: {username}, {password}")
            user_data = self.db_manager.get_user_role(username, password)
            print(f"User data: {user_data}")

            if user_data:
                user = User(username, user_data[0]['RoleName'])
                client_socket.send(f"Login successful! Your role is {user.role}.\n".encode())
                client_socket.send(f"Available functionalities: {', '.join(user.get_role_functions())}\n".encode())

                while True:
                    client_socket.send(
                        "Press the given numbers to perform the actions:\n1. Add Food Item\n2. Delete Food Item\n3. Update Food Item\n4. View Food Items\n5. Exit\n".encode())
                    command = client_socket.recv(1024).decode().strip()
                    print(f"Received command: {command}")
                    if command == '5':
                        break
                    self.command_handler.handle_command(user, command, client_socket)
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
    command_handler = CommandHandler(db_manager)
    server = Server("0.0.0.0", 8889, db_manager, command_handler)
    server.start()
