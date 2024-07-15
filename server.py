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
            username, password = user_credentials.split('|')
            user_data = self.db_manager.get_user_role(username, password)

            if user_data:
                user = User(user_data[0]['Id'], username, user_data[0]['RoleName'])
                client_socket.send(f"Login successful! Your role is {user.role}. Your user ID is {user.user_id}.\n".encode())

                while True:
                    if user.role == 'Admin':
                        client_socket.send("Press the given numbers to perform the actions:\n1. Add Food Item\n2. Delete Food Item\n3. Update Food Item\n4. View Food Items\n5. Exit\n".encode())
                    elif user.role == 'Chef':
                        client_socket.send("Press the given numbers to perform the actions:\n1. Check Voting Result\n2. Discard/Delete Items\n3. View Menu\n4. Rollout Recommendations\n5. Exit\n".encode())
                    elif user.role == 'Employee':
                        client_socket.send("Press the given numbers to perform the actions:\n1. View Notifications\n2. Give Feedback\n3. View Menu\n4. Choose Food Item for Tomorrow\n5. Add Mom's Recipe\n6. For EXIT\n".encode())

                    command = client_socket.recv(1024).decode().strip()
                    if command == '5' and user.role != 'Employee' or command == '6' and user.role == 'Employee':
                        break
                    self.command_handler.handle_command(user, command, client_socket)
            else:
                client_socket.send("Invalid credentials.\n".encode())
        except socket.error as e:
            print(f"Socket error: {e}")
            client_socket.send(f"Socket error occurred: {e}\n".encode())
        except ValueError as e:
            print(f"Value error: {e}")
            client_socket.send(f"Invalid input format: {e}\n".encode())
        except Exception as e:
            print(f"Error: {e}")
            client_socket.send(f"An error occurred: {e}\n".encode())
        finally:
            client_socket.close()

    def start(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.address, self.port))
            server.listen(5)
            print(f"Server started on port {self.port}")
            while True:
                client_socket, addr = server.accept()
                print(f"Accepted connection from {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except socket.error as e:
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.close()


if __name__ == "__main__":
    db_manager = DatabaseManager()
    command_handler = CommandHandler(db_manager)
    server = Server("0.0.0.0", 7778, db_manager, command_handler)
    server.start()
