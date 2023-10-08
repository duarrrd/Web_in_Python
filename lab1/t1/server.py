import socket
import threading
import datetime

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port for the server
host = '127.0.0.1'  # localhost
port = 12345
Check = True 
# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)

print("Server is waiting for connections...")

def handle_client(client_socket, client_address):
    """Handles a single client connection."""
    global Check

    while Check:
        print(f"Connection established with {client_address}")
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')

        if not data:
            break

        # Get the current time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print the received data and the time it was received
        print(f"Received: {data} from {client_address} at {current_time}")

        # Check if the client sent a specific shutdown message
        if data.strip().lower() == 'shutdown':
            print("Server is shutting down...")
            Check = False
            break

        # Simulate a 5-second delay
        import time
        time.sleep(5)

        # Check if all data was sent successfully (based on data size)
        if len(data) == client_socket.send(data.encode('utf-8')):
            print(f"Data sent successfully to {client_address}.")
        else:
            print(f"Error: Data transmission issue to {client_address}.")
            break

    # Close the client socket
    client_socket.close()

# Accept connections from clients and create a new thread for each client
while Check:
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

# Close the server socket
server_socket.close()
