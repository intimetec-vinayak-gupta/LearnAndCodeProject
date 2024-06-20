import socket

def main():
    server_address = "127.0.0.1"
    server_port = 8889

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_address, server_port))
        print(f"Connected to server at {server_address}:{server_port}")

        username = input("Enter username: ")
        password = input("Enter password: ")
        userCredentials = f"{username}|{password}"
        client_socket.send(userCredentials.encode())

        while True:

            server_message = client_socket.recv(1024).decode()
            if not server_message:
                break
            print(server_message)

            if "Enter" in server_message or "Press" in server_message:
                user_input = input()
                client_socket.send(user_input.encode())

                if user_input == '1':  # Checking if the user selected option 1 to add a food item
                    item_name = input("Enter Food Item Name: ")
                    item_price = input("Enter Food Item Price: ")
                    item_category = input("Enter Food Item Category (as an integer): ")

                    # Send all data at once, separated by a delimiter (e.g., "|")
                    all_inputs = f"{item_name}|{item_price}|{item_category}"
                    client_socket.send(all_inputs.encode())
                elif user_input == '2':
                    item_id = input("Enter Food Item Id to DELETE: ")
                    client_socket.send(item_id.encode())
                elif user_input == '3':
                    item_id = input("Enter Food Item Id to UPDATE Availability Status: ")
                    availability_status = input("Enter Availability Status: ")
                    all_inputs = f"{item_id}|{availability_status}"
                    print(all_inputs)
                    client_socket.send(all_inputs.encode())

    except socket.error as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Disconnected from server")


if __name__ == "__main__":
    main()
