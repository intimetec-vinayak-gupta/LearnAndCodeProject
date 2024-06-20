import socket
import threading
import mysql.connector
import time

# MySQL database connection configuration
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

def add_food_item(item_name, item_price, item_category):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO FoodItems (Name, Price, Category) VALUES (%s, %s, %s)"
        cursor.execute(query, (item_name, item_price, item_category))
        connection.commit()
        #print(f"Added item: {item_name}, Price: {item_price}, Category: {item_category}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def delete_food_item(item_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "DELETE FROM FoodItems WHERE Id = %s"
        cursor.execute(query, (item_id,))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def update_food_item(item_id, availability_status):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "UPDATE FoodItems SET IsAvailable = %s WHERE Id = %s"
        cursor.execute(query, (availability_status, item_id))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def view_food_items():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM FoodItems"
        cursor.execute(query)
        items = cursor.fetchall()
        return items
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_user_role(username, password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.Name AS UserName, r.Name AS RoleName 
            FROM Users u 
            JOIN Roles r ON u.RoleId = r.Id  
            JOIN UsersCredentials uc ON u.Id = uc.UserId 
            WHERE u.Name = %s AND uc.Password = %s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def handle_client(client_socket):
    try:
        userCredentials = client_socket.recv(1024).decode().strip()
        username, password = userCredentials.split('|')
        user = get_user_role(username, password)

        if user:
            role = user["RoleName"]
            client_socket.send(f"Login successful! Your role is {role}.\n".encode())
            client_socket.send(f"Available functionalities: {', '.join(role_functions[role])}\n".encode())

            if role == "Admin":
                while True:
                    client_socket.send(
                        "Press the given numbers to perform the actions:\n1. Add Food Item\n2. Delete Food Item\n3. Update Food Item\n4. View Food Items\n5. Exit\n".encode())
                    choice = client_socket.recv(1024).decode().strip()

                    if choice == '1':
                        all_inputs = client_socket.recv(1024).decode().strip()
                        item_name, item_price, item_category = all_inputs.split('|')
                        item_price = float(item_price)
                        item_category = int(item_category)
                        add_food_item(item_name, item_price, item_category)
                        client_socket.send(f"Food item '{item_name}' added successfully.\n".encode())

                    elif choice == '2':
                        item_id = int(client_socket.recv(1024).decode().strip())
                        delete_food_item(item_id)
                        client_socket.send(f"Food item with Id '{item_id}' deleted successfully.\n".encode())

                    elif choice == '3':
                        all_inputs = client_socket.recv(1024).decode().strip()
                        item_id, availability_status = all_inputs.split('|')
                        item_id = int(item_id)
                        availability_status = int(availability_status)
                        update_food_item(item_id, availability_status)
                        client_socket.send(
                            f"Food item with Id '{item_id}' updated successfully, the IsAvailable changed to '{availability_status}'.\n".encode())
                    elif choice == '4':
                        items = view_food_items()
                        #print(f"Fetched items from DB: {items}")  # Debugging statement
                        if items:
                            client_socket.send("Food Items:\n".encode())
                            for item in items:
                                #print(f"Sending item: {item}")  # Debugging statement
                                client_socket.send(f"Id: {item['Id']}, Name: {item['Name']}\n".encode())
                                # Adding a small delay to prevent overwhelming the client
                                time.sleep(0.1)
                        else:
                            client_socket.send("No food items found.\n".encode())
                    elif choice == '5':
                        break
                    else:
                        client_socket.send("Invalid choice.\n".encode())
        else:
            client_socket.send("Invalid credentials.\n".encode())
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8889))  # Changed port number to 8889
    server.listen(500)
    print("Server started on port 8889")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
