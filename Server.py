import socket
import threading
import mysql.connector
# MySQL database connection
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'LearnAndCode_Project'
}
# Role-based functionalities
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
def get_user_role(username, password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT u.Name AS UserName, r.Name AS RoleName FROM Users u JOIN Roles r ON u.RoleId = r.Id  JOIN UsersCredentials uc ON u.Id = uc.UserId WHERE u.Name = %s AND   uc.Password = %s"
        cursor.execute(query, [username, password])
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def handle_client(client_socket):
    try:
        client_socket.send("Enter username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        client_socket.send("Enter password: ".encode())
        password = client_socket.recv(1024).decode().strip()
        user = get_user_role(username, password)
        
        if user:
            role = user["RoleName"]
            client_socket.send(f"Login successful! Your role is {role}.\n".encode())
            client_socket.send(f"Available functionalities: {', '.join(role_functions[role])}\n".encode())
        else:
            client_socket.send("Invalid credentials.\n".encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server started on port 9999")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr} , {client_socket}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()