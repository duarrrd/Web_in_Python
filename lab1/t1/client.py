import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server host and port to connect to
server_host = '127.0.0.1'  # localhost
server_port = 12345

# Connect to the server
client_socket.connect((server_host, server_port))

while True:
    # Get input from the user
    sentence = input("Enter a sentence (or 'exit' to quit): ")
    
    # Send the input to the server
    client_socket.send(sentence.encode('utf-8'))
    
    if sentence.lower() == 'exit':
        break

    # Receive and print the echoed data from the server
    echoed_data = client_socket.recv(1024).decode('utf-8')
    print(f"Server echoed: {echoed_data}")

# Close the client socket
client_socket.close()
