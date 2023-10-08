import socket
import threading

# Function to receive and display messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connection to the server has been lost.")
            client_socket.close()
            break

# Function to send messages to the server
def send_message(client_socket, nickname):
    while True:
        message = input()
        if message.lower() == "/exit":
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
            break
        else:
            client_socket.send((nickname + ": " + message).encode('utf-8'))

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Automatically connect to the server at 127.0.0.1:12345
server_address = ("127.0.0.1", 12345)
client_socket.connect(server_address)

# Get the user's nickname
nickname = input("Enter your nickname: ")

# Start separate threads for receiving and sending messages
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
send_thread = threading.Thread(target=send_message, args=(client_socket, nickname))

receive_thread.start()
send_thread.start()
