import socket
import datetime

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port for the server
host = '127.0.0.1'  # localhost
port = 12345

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)

print("Server is waiting for a connection...")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()

print(f"Connection established with {client_address}")

while True:
    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    
    if not data:
        break
    
    # Get the current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Print the received data and the time it was received
    print(f"Received: {data} at {current_time}")

# Close the connection and the server socket
client_socket.close()
server_socket.close()
