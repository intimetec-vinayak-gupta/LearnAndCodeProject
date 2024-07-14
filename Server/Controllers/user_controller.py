from Controllers.admin_command_handler import AdminCommandHandler
from Controllers.chef_command_handler import ChefCommandHandler
from Controllers.employee_command_handler import EmployeeCommandHandler
from DBManagement.database_manager import DatabaseManager


class UserController:

    def handle_command(self, user, client_socket):
        if user.role == "Admin":
            client_socket.send("Press the given numbers to perform the actions:\n1. Add Food Item\n2. Delete Food Item\n3. Update Food Item\n4. View Food Items\n5. Exit\n".encode())
            command = client_socket.recv(1024).decode().strip()
            admin_handler = AdminCommandHandler(DatabaseManager)
            admin_handler.handle_command(command, client_socket)
        elif user.role == "Chef":
            client_socket.send("Press the given numbers to perform the actions:\n1. Check Voting Result\n2. Discard/Delete Items\n3. View Menu\n4. Rollout Recommendations\n5. Exit\n".encode())
            command = client_socket.recv(1024).decode().strip()
            chef_handler = ChefCommandHandler(DatabaseManager)
            chef_handler.handle_command(command, client_socket)
        elif user.role == "Employee":
            client_socket.send("Press the given numbers to perform the actions:\n1. View Notifications\n2. Give Feedback\n3. View Menu\n4. Choose Food Item for Tomorrow\n5. Add Mom's Recipe\n6. For EXIT\n".encode())
            command = client_socket.recv(1024).decode().strip()
            employee_handler = EmployeeCommandHandler(DatabaseManager)
            employee_handler.handle_command(command, client_socket)