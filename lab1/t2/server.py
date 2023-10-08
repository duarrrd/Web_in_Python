import socket
import threading

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))  # Change the IP and port as needed
server_socket.listen(5)
print("Server is waiting for connections...")
# List to hold connected clients
clients = []

# Function to broadcast messages to all connected clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the client if unable to send a message
                remove(client)

# Function to remove a client from the list
def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# Function to handle client connections
def client_thread(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                remove(client_socket)
                break
            else:
                broadcast(message, client_socket)
        except:
            continue

# Main server loop
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Client {client_address} connected.")
    client_thread_handler = threading.Thread(target=client_thread, args=(client_socket,))
    client_thread_handler.start()